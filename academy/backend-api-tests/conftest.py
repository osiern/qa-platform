"""Общие fixtures для всех модулей.

Правила, которые проверяют на собеседовании:
- каждый тест создаёт свои данные и удаляет только их;
- тяжёлые подключения (БД, Redis, gRPC) открываются один раз на сессию — scope='session';
- данные пользователя живут один тест — scope='function' (по умолчанию);
- yield делит fixture на подготовку и очистку: код после yield выполнится даже при падении теста.
"""
import uuid

import pytest

from clients import settings
from clients.api import ShopApi
from clients.cache import Cache
from clients.compose import Compose
from clients.db import Db
from clients.events import PaymentTopic
from clients.inventory import InventoryClient

PASSWORD = 'Study-password-123'


@pytest.fixture(scope='session')
def db():
    client = Db(settings.DATABASE_URL)
    yield client
    client.close()


@pytest.fixture(scope='session')
def cache():
    client = Cache(settings.REDIS_URL)
    yield client
    client.close()


@pytest.fixture(scope='session')
def inventory():
    client = InventoryClient(settings.GRPC_TARGET)
    yield client
    client.close()


@pytest.fixture(scope='session')
def compose():
    return Compose()


@pytest.fixture
def api():
    """Анонимный клиент: без токена."""
    client = ShopApi(settings.BASE_URL)
    yield client
    client.close()


@pytest.fixture(scope='session')
def admin():
    client = ShopApi(settings.BASE_URL)
    assert client.login(settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD).status_code == 200
    yield client
    client.logout()
    client.close()


@pytest.fixture
def new_email():
    return f'stack-{uuid.uuid4().hex}@example.test'


@pytest.fixture
def user(db, cache, new_email):
    """Зарегистрированный и вошедший пользователь. После теста удаляются он, его заказы и ключи Redis."""
    client = ShopApi(settings.BASE_URL)
    created = client.register(new_email, PASSWORD)
    assert created.status_code == 201, created.text
    assert client.login(new_email, PASSWORD).status_code == 200
    client.user['password'] = PASSWORD
    yield client
    user_id = created.json()['id']
    cache.delete_user_data(user_id)
    # ON DELETE CASCADE удаляет заказы, позиции, outbox и payment_events этого пользователя.
    db.execute('DELETE FROM users WHERE id=%s AND email=%s', (user_id, new_email))
    client.close()


@pytest.fixture
def make_product(admin, db):
    """Фабрика товаров: fixture возвращает функцию, тест создаёт столько товаров, сколько нужно."""
    created = []

    def factory(**overrides) -> dict:
        body = {'name': f'Учебный товар {uuid.uuid4().hex[:8]}', 'category': 'accessories',
                'price': 123400, 'stock': 10, 'description': 'Товар одного теста', **overrides}
        response = admin.create_product(**body)
        assert response.status_code == 201, response.text
        created.append(response.json()['id'])
        return response.json()

    yield factory
    for product_id in created:
        # Позиции заказов ссылаются на товар без каскада — сначала удаляем их.
        db.execute('DELETE FROM order_items WHERE product_id=%s', (product_id,))
        db.execute('DELETE FROM products WHERE id=%s', (product_id,))


@pytest.fixture
def product(make_product):
    return make_product()


@pytest.fixture
def order(user, product):
    """Заказ в статусе new на одну единицу товара."""
    assert user.put_cart(product['id'], 1).status_code == 200
    response = user.create_order('Самара, Учебная улица, 10')
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
def payments():
    topic = PaymentTopic(settings.KAFKA_BOOTSTRAP, settings.PAYMENT_TOPIC)
    topic.move_to_end()
    yield topic
    topic.close()
