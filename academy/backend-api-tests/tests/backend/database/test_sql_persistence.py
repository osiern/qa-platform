"""Verify relational data written by the API."""
import uuid

import allure
import pytest

pytestmark = [pytest.mark.sql, allure.feature('SQL persistence')]


@allure.title('SELECT … WHERE: регистрация через API создала одну строку с хешем пароля')
def test_user_row_after_registration(user, db):
    row = db.one('SELECT email, role, password_hash FROM users WHERE id=%s', (user.user['id'],))

    assert (row['email'], row['role']) == (user.user['email'], 'customer')
    assert user.user['password'] not in row['password_hash'], 'Пароль не должен храниться открытым текстом'


@allure.title('JOIN: позиции заказа связаны с заказом и товаром')
def test_order_join_items_and_products(user, make_product, db):
    first, second = make_product(price=1000), make_product(price=2500)
    user.put_cart(first['id'], 2)
    user.put_cart(second['id'], 1)
    order = user.create_order('Самара, Учебная улица, 10').json()

    rows = db.all(
        """
        SELECT p.name, oi.quantity, oi.price
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        JOIN products p ON p.id = oi.product_id
        WHERE o.id = %s
        ORDER BY p.price
        """,
        (order['id'],),
    )

    assert rows == [
        {'name': first['name'], 'quantity': 2, 'price': 1000},
        {'name': second['name'], 'quantity': 1, 'price': 2500},
    ]


@allure.title('GROUP BY + SUM: сумма заказа в orders равна сумме позиций')
def test_order_total_equals_sum_of_items(user, make_product, db):
    for price, quantity in ((1000, 3), (2500, 2)):
        product = make_product(price=price)
        user.put_cart(product['id'], quantity)
    order = user.create_order('Самара, Учебная улица, 10').json()

    row = db.one(
        """
        SELECT o.total, SUM(oi.price * oi.quantity) AS items_sum, COUNT(*) AS positions
        FROM orders o JOIN order_items oi ON oi.order_id = o.id
        WHERE o.id = %s
        GROUP BY o.id
        """,
        (order['id'],),
    )

    assert row == {'total': 8000, 'items_sum': 8000, 'positions': 2}


@allure.title('Цена в позиции фиксируется на момент покупки')
def test_item_price_is_snapshot(user, product, db, admin):
    user.put_cart(product['id'], 1)
    order = user.create_order('Самара, Учебная улица, 10').json()

    db.execute('UPDATE products SET price = price * 2 WHERE id=%s', (product['id'],))

    assert db.scalar('SELECT price FROM order_items WHERE order_id=%s', (order['id'],)) == product['price']


@allure.title('LEFT JOIN: у нового пользователя ноль заказов, а не отсутствие строки')
def test_left_join_counts_zero(user, db):
    row = db.one(
        """
        SELECT u.email, COUNT(o.id) AS orders
        FROM users u LEFT JOIN orders o ON o.user_id = u.id
        WHERE u.id = %s
        GROUP BY u.email
        """,
        (user.user['id'],),
    )

    assert row['orders'] == 0


@allure.title('Подзапрос: остаток товара уменьшился ровно на купленное количество')
def test_stock_decrease_by_subquery(user, make_product, db):
    product = make_product(stock=10)
    user.put_cart(product['id'], 4)
    user.create_order('Самара, Учебная улица, 10')

    remaining = db.scalar(
        """
        SELECT p.stock + (SELECT COALESCE(SUM(quantity), 0) FROM order_items WHERE product_id = p.id)
        FROM products p WHERE p.id = %s
        """,
        (product['id'],),
    )

    assert remaining == 10, 'Остаток + проданное = исходный остаток'


@allure.title('Параметры запроса: строка с SQL остаётся данными, инъекции нет')
def test_parameters_prevent_sql_injection(db):
    hostile = "x' OR '1'='1"

    rows = db.all('SELECT id FROM users WHERE email = %s', (hostile,))

    assert rows == []


@allure.title('Найдено: поиск API не экранирует % и _ в LIKE')
@pytest.mark.xfail(strict=True, reason='Найденный дефект: q подставляется в ILIKE без экранирования, '
                                       '"%" находит все товары. Ожидаемо — только названия с символом %.')
def test_search_escapes_like_wildcards(api, make_product):
    make_product(name=f'Обычный товар {uuid.uuid4().hex[:6]}')

    names = [item['name'] for item in api.products(q='%', limit=100).json()]

    assert all('%' in name for name in names)
