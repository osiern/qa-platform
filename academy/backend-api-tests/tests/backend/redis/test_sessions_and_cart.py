"""Redis session and cart behavior."""
import allure
import pytest

from clients import settings

pytestmark = [pytest.mark.redis, allure.feature('Redis')]


@allure.title('Вход создаёт строковый ключ session:{token} → id пользователя с TTL')
def test_login_creates_session(user, cache):
    key = f'session:{user.token}'

    assert cache.type(key) == 'string'
    assert cache.get(key) == str(user.user['id'])
    assert settings.SESSION_TTL - 60 < cache.ttl(key) <= settings.SESSION_TTL


@allure.title('Выход удаляет ключ сессии: TTL -2 значит «ключа нет»')
def test_logout_deletes_session(user, cache):
    key = f'session:{user.token}'
    user.logout()

    assert cache.ttl(key) == -2


@allure.title('Удалённый вручную ключ сессии разлогинивает пользователя')
def test_deleted_session_means_401(user, cache):
    cache.redis.delete(f'session:{user.token}')

    assert user.me().status_code == 401


@allure.title('Корзина — hash product_id → количество с TTL сутки')
def test_cart_is_hash_with_ttl(user, make_product, cache):
    first, second = make_product(), make_product()
    user.put_cart(first['id'], 2)
    user.put_cart(second['id'], 1)
    key = f"cart:{user.user['id']}"

    assert cache.type(key) == 'hash'
    assert cache.hgetall(key) == {str(first['id']): '2', str(second['id']): '1'}
    assert settings.CART_TTL - 60 < cache.ttl(key) <= settings.CART_TTL


@allure.title('Значения в Redis — строки: количество хранится как "2", а не 2')
def test_redis_stores_strings(user, product, cache):
    user.put_cart(product['id'], 2)

    value = cache.hgetall(f"cart:{user.user['id']}")[str(product['id'])]

    assert isinstance(value, str)


@allure.title('Удаление позиции: HDEL оставляет остальные поля hash')
def test_remove_from_cart_hdel(user, make_product, cache):
    keep, remove = make_product(), make_product()
    user.put_cart(keep['id'], 1)
    user.put_cart(remove['id'], 1)

    user.remove_from_cart(remove['id'])

    assert cache.hgetall(f"cart:{user.user['id']}") == {str(keep['id']): '1'}


@allure.title('Заказ очищает корзину: ключа больше нет')
def test_checkout_deletes_cart(user, order, cache):
    assert not cache.exists(f"cart:{user.user['id']}")


@allure.title('Избранное — set: повторное добавление не создаёт дубль, TTL нет')
def test_favorites_is_set(user, product, cache):
    user.add_favorite(product['id'])
    user.add_favorite(product['id'])
    key = f"favorites:{user.user['id']}"

    assert cache.type(key) == 'set'
    assert cache.smembers(key) == {str(product['id'])}
    assert cache.ttl(key) == -1


@allure.title('Источник правды: API читает корзину из Redis, а не из БД')
def test_api_reads_cart_from_redis(user, product, cache):
    cache.redis.hset(f"cart:{user.user['id']}", str(product['id']), '5')

    assert user.cart().json()['items'][0]['quantity'] == 5
