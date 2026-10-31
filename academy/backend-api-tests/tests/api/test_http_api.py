"""HTTP API contract, validation, authorization and order workflows."""
import uuid

import allure
import httpx
import pytest

from clients import settings
from clients.models import CartView, LoginView, OrderView, ProductView, UserView

pytestmark = [pytest.mark.api, allure.feature('HTTP / REST API')]


@allure.title('201 Created: регистрация возвращает пользователя по контракту')
def test_register_returns_201_and_contract(api, db, new_email):
    response = api.register(new_email, 'Study-password-123')
    try:
        assert response.status_code == 201
        user = UserView.model_validate(response.json())
        assert (user.email, user.role) == (new_email, 'customer')
    finally:
        db.execute('DELETE FROM users WHERE email=%s', (new_email,))


@allure.title('Сервер нормализует email: пробелы и регистр не создают второго пользователя')
def test_email_is_normalized(api, user):
    response = api.register('  ' + user.user['email'].upper() + ' ', 'Study-password-123')

    assert response.status_code == 409
    assert response.json() == {'detail': 'Email уже зарегистрирован'}


@allure.title('200 OK: вход выдаёт токен по контракту')
def test_login_contract(api, user):
    response = api.login(user.user['email'], user.user['password'])

    assert response.status_code == 200
    assert LoginView.model_validate(response.json()).expires_in == settings.SESSION_TTL


@allure.title('401: одинаковый ответ для неверного пароля и несуществующего email')
def test_login_errors_do_not_reveal_users(api, user):
    wrong_password = api.login(user.user['email'], 'Wrong-password-123')
    unknown_email = api.login(f'nobody-{uuid.uuid4().hex}@example.test', 'Wrong-password-123')

    assert wrong_password.status_code == unknown_email.status_code == 401
    assert wrong_password.json() == unknown_email.json()


@allure.title('401 без токена, 401 с чужим токеном, 403 без прав администратора')
@pytest.mark.parametrize(
    ('token', 'status'),
    [pytest.param(None, 401, id='без заголовка'), pytest.param('forged-token', 401, id='поддельный токен')],
)
def test_protected_endpoint_requires_session(token, status):
    client = httpx.Client(base_url=settings.BASE_URL + '/api')
    headers = {'Authorization': f'Bearer {token}'} if token else {}

    assert client.get('/cart', headers=headers).status_code == status


def test_customer_cannot_create_products(user):
    response = user.create_product(name='Чужой товар', category='audio', price=100, stock=1)

    assert response.status_code == 403


@allure.title('404: несуществующий товар; 422: id не число')
def test_not_found_and_validation(api):
    assert api.product(999999999).status_code == 404
    assert api.request('GET', '/products/abc').status_code == 422


@allure.title('Query-параметры: поиск и сортировка по цене')
def test_search_and_sort(api, make_product):
    prefix = f'Сортировка {uuid.uuid4().hex[:6]}'
    for price in (3000, 1000, 2000):
        make_product(name=f'{prefix} {price}', price=price)

    response = api.products(q=prefix, sort='price_asc')

    assert [ProductView.model_validate(item).price for item in response.json()] == [1000, 2000, 3000]


@allure.title('422: недопустимое значение sort отклоняется схемой')
def test_invalid_sort_is_rejected(api):
    assert api.products(sort='name').status_code == 422


@allure.title('PUT идемпотентен: повтор с тем же телом не меняет корзину')
def test_put_cart_is_idempotent(user, product):
    first = user.put_cart(product['id'], 2)
    second = user.put_cart(product['id'], 2)

    assert first.json() == second.json()
    assert CartView.model_validate(second.json()).total == product['price'] * 2


@allure.title('422: StrictInt — количество строкой "2" не принимается')
@pytest.mark.parametrize('quantity', [0, 100, '2', 1.5], ids=['ноль', 'больше 99', 'строка', 'дробное'])
def test_cart_quantity_validation(user, product, quantity):
    assert user.put_cart(product['id'], quantity).status_code == 422


@allure.title('409: количество больше остатка')
def test_cart_over_stock(user, make_product):
    product = make_product(stock=2)

    response = user.put_cart(product['id'], 3)

    assert response.status_code == 409
    assert response.json()['detail'] == 'Недостаточно товара'


@allure.title('Idempotency-Key: повтор запроса возвращает тот же заказ, а не создаёт второй')
def test_order_idempotency_key(user, product):
    user.put_cart(product['id'], 1)
    key = uuid.uuid4().hex

    first = user.create_order('Самара, Учебная улица, 10', key=key)
    repeat = user.create_order('Самара, Учебная улица, 10', key=key)

    assert (first.status_code, repeat.status_code) == (201, 201)
    assert repeat.json()['id'] == first.json()['id']
    assert len(user.orders().json()) == 1


@allure.title('409: тот же Idempotency-Key с другими параметрами')
def test_idempotency_key_conflict(user, product):
    user.put_cart(product['id'], 1)
    key = uuid.uuid4().hex
    user.create_order('Самара, Учебная улица, 10', key=key)

    response = user.create_order('Казань, Другая улица, 5', key=key)

    assert response.status_code == 409


@allure.title('422: без обязательного заголовка Idempotency-Key')
def test_order_requires_idempotency_header(user, product):
    user.put_cart(product['id'], 1)

    response = user.request('POST', '/orders', body={'address': 'Самара, Учебная улица, 10'})

    assert response.status_code == 422


@allure.title('Изоляция: чужой заказ отдаётся как 404, а не 403')
def test_foreign_order_is_hidden(order, api, db, cache, new_email):
    stranger = api
    stranger.register(new_email.replace('stack-', 'stranger-'), 'Study-password-123')
    stranger.login(new_email.replace('stack-', 'stranger-'), 'Study-password-123')
    try:
        # 404 не подтверждает, что заказ с таким id вообще существует.
        assert stranger.order(order['id']).status_code == 404
        assert stranger.cancel(order['id']).status_code == 404
    finally:
        cache.delete_user_data(stranger.user['id'])
        db.execute('DELETE FROM users WHERE id=%s', (stranger.user['id'],))


@allure.title('Контракт заказа и переход статуса new → cancelled')
def test_order_contract_and_cancel(user, order):
    assert OrderView.model_validate(order).status == 'new'

    cancelled = user.cancel(order['id'])

    assert cancelled.status_code == 200
    assert cancelled.json()['status'] == 'cancelled'


@allure.title('204 No Content: выход без тела, старый токен больше не работает')
def test_logout(user):
    response = user.logout()

    assert response.status_code == 204
    assert response.content == b''
    assert user.me().status_code == 401


@allure.title('OpenAPI: схема доступна и описывает ключевые пути')
def test_openapi_schema():
    schema = httpx.get(settings.BASE_URL + '/openapi.json').json()

    assert {'/api/users', '/api/login', '/api/orders', '/api/orders/{oid}/pay'} <= set(schema['paths'])
