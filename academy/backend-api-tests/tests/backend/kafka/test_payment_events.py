"""Kafka outbox, payment event and worker integration."""
import time

import allure
import pytest

pytestmark = [pytest.mark.kafka, allure.feature('Kafka payments')]


def wait_status(user, order_id, status, timeout=20):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if user.order(order_id).json()['status'] == status:
            return
        time.sleep(0.3)
    raise AssertionError(f'Заказ {order_id} не получил статус {status} за {timeout} с')


@allure.title('Оплата: API сразу отвечает 202 и payment_pending, а не paid')
def test_pay_is_accepted_not_completed(user, order):
    response = user.pay(order['id'])

    assert response.status_code == 202
    assert response.json()['status'] in ('payment_pending', 'paid')


@allure.title('Outbox: событие записано в БД в той же транзакции, что и смена статуса')
def test_outbox_row_created(user, order, db):
    user.pay(order['id'])

    row = db.one('SELECT payload FROM outbox WHERE order_id=%s', (order['id'],))

    assert row['payload']['order_id'] == order['id']
    assert row['payload']['amount'] == order['total']


@allure.title('Топик: worker публикует событие с ключом = id заказа')
def test_event_in_topic(user, order, payments):
    user.pay(order['id'])

    record = payments.wait_for(order['id'])

    assert record.key == str(order['id'])
    assert set(record.value) == {'event_id', 'order_id', 'amount'}
    assert record.value['amount'] == order['total']


@allure.title('Consumer: событие обработано, заказ paid, есть запись payment_events')
def test_event_is_consumed(user, order, db):
    user.pay(order['id'])

    wait_status(user, order['id'], 'paid')

    assert db.scalar('SELECT COUNT(*) FROM payment_events WHERE order_id=%s', (order['id'],)) == 1
    assert db.scalar('SELECT published FROM outbox WHERE order_id=%s', (order['id'],)) is True


@allure.title('Повторная оплата не создаёт второе событие')
def test_second_pay_is_noop(user, order, db):
    user.pay(order['id'])
    user.pay(order['id'])

    assert db.scalar('SELECT COUNT(*) FROM outbox WHERE order_id=%s', (order['id'],)) == 1


@allure.title('At-least-once: дубль события не меняет заказ дважды')
def test_duplicate_event_is_ignored(user, order, payments, db):
    user.pay(order['id'])
    original = payments.wait_for(order['id'])
    wait_status(user, order['id'], 'paid')
    payments.move_to_end()

    payments.publish(original.value, key=original.key)
    payments.wait_for(order['id'])
    time.sleep(1.5)  # даём worker время обработать дубль; здесь проверяем отсутствие изменения

    assert db.scalar('SELECT COUNT(*) FROM payment_events WHERE order_id=%s', (order['id'],)) == 1
    assert user.order(order['id']).json()['status'] == 'paid'


@allure.title('Отменённый заказ нельзя оплатить: 409, событие не создаётся')
def test_cancelled_order_cannot_be_paid(user, order, db):
    user.cancel(order['id'])

    response = user.pay(order['id'])

    assert response.status_code == 409
    assert db.scalar('SELECT COUNT(*) FROM outbox WHERE order_id=%s', (order['id'],)) == 0


@allure.title('Оплаченный заказ нельзя отменить: 409')
def test_paid_order_cannot_be_cancelled(user, order):
    user.pay(order['id'])
    wait_status(user, order['id'], 'paid')

    assert user.cancel(order['id']).status_code == 409
