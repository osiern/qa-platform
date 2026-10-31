"""Cross-service integration: an order flows through HTTP → PostgreSQL → Redis → gRPC → Kafka → worker.

Это ответ на вопрос «как проверить, что система работает под капотом, а не только экран».
"""
import time

import allure
import pytest

from clients.models import OrderView

pytestmark = [pytest.mark.e2e, allure.feature('Order flow across services')]


@allure.title('Заказ и оплата через все слои системы')
def test_order_through_all_layers(user, make_product, db, cache, inventory, payments):
    product = make_product(price=150000, stock=5)
    user_id = user.user['id']

    with allure.step('HTTP: положить 2 шт. в корзину'):
        assert user.put_cart(product['id'], 2).status_code == 200

    with allure.step('Redis: корзина лежит в hash cart:{user_id}'):
        assert cache.hgetall(f'cart:{user_id}') == {str(product['id']): '2'}

    with allure.step('HTTP: оформить заказ'):
        response = user.create_order('Самара, Учебная улица, 10')
        assert response.status_code == 201
        order = OrderView.model_validate(response.json())

    with allure.step('PostgreSQL: заказ и позиция записаны, остаток списан'):
        assert db.scalar('SELECT total FROM orders WHERE id=%s', (order.id,)) == 300000
        assert db.scalar('SELECT stock FROM products WHERE id=%s', (product['id'],)) == 3

    with allure.step('Redis: корзина удалена после заказа'):
        assert not cache.exists(f'cart:{user_id}')

    with allure.step('gRPC: Inventory видит тот же остаток'):
        assert inventory.get_stock(product['id'], token=user.token).available == 3

    with allure.step('HTTP: оплатить — 202, обработка асинхронная'):
        assert user.pay(order.id).status_code == 202

    with allure.step('Kafka: в топике событие с суммой заказа'):
        record = payments.wait_for(order.id)
        assert record.value['amount'] == 300000

    with allure.step('Worker: заказ стал paid'):
        deadline = time.monotonic() + 20
        while user.order(order.id).json()['status'] != 'paid':
            assert time.monotonic() < deadline, 'worker не обработал оплату за 20 с'
            time.sleep(0.3)

    with allure.step('PostgreSQL: событие оплаты сохранено ровно один раз'):
        row = db.one('SELECT event_id, amount FROM payment_events WHERE order_id=%s', (order.id,))
        assert row == {'event_id': record.value['event_id'], 'amount': 300000}
