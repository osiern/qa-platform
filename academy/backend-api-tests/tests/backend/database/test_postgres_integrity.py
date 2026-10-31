"""PostgreSQL constraints, transactions, locking and concurrent checkout."""
import threading
import uuid

import allure
import psycopg
import pytest
from psycopg import errors

from clients import settings

pytestmark = [pytest.mark.postgres, allure.feature('PostgreSQL integrity')]


@allure.title('CHECK: база не даст сделать остаток отрицательным, даже если API ошибётся')
def test_check_constraint_stock(db, product):
    with pytest.raises(errors.CheckViolation):
        with db.transaction() as connection:
            connection.execute('UPDATE products SET stock = -1 WHERE id=%s', (product['id'],))


@allure.title('UNIQUE: второй пользователь с тем же email — UniqueViolation')
def test_unique_email(db, user):
    with pytest.raises(errors.UniqueViolation):
        with db.transaction() as connection:
            connection.execute("INSERT INTO users (email, password_hash, name, role) VALUES (%s, 'x', 'x', 'customer')",
                               (user.user['email'],))


@allure.title('FOREIGN KEY: позиция заказа не может ссылаться на несуществующий заказ')
def test_foreign_key(db, product):
    with pytest.raises(errors.ForeignKeyViolation):
        with db.transaction() as connection:
            connection.execute('INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (-1, %s, 1, 1)',
                               (product['id'],))


@allure.title('ROLLBACK: изменения внутри упавшей транзакции не сохраняются')
def test_rollback(db, product):
    with pytest.raises(RuntimeError):
        with db.transaction() as connection:
            connection.execute('UPDATE products SET stock = 0 WHERE id=%s', (product['id'],))
            raise RuntimeError('ошибка посреди транзакции')

    assert db.scalar('SELECT stock FROM products WHERE id=%s', (product['id'],)) == product['stock']


@allure.title('READ COMMITTED: другое соединение не видит незакоммиченных изменений')
def test_uncommitted_changes_are_invisible(db, product):
    with psycopg.connect(settings.DATABASE_URL) as writer:
        writer.execute('UPDATE products SET stock = 0 WHERE id=%s', (product['id'],))

        seen_before_commit = db.scalar('SELECT stock FROM products WHERE id=%s', (product['id'],))
        writer.rollback()

    assert seen_before_commit == product['stock']


@allure.title('SELECT … FOR UPDATE: вторая транзакция ждёт блокировку строки')
def test_row_lock(db, product):
    with psycopg.connect(settings.DATABASE_URL) as holder, psycopg.connect(settings.DATABASE_URL) as waiter:
        holder.execute('SELECT id FROM products WHERE id=%s FOR UPDATE', (product['id'],))
        waiter.execute("SET lock_timeout = '300ms'")

        with pytest.raises(errors.LockNotAvailable):
            waiter.execute('UPDATE products SET stock = stock - 1 WHERE id=%s', (product['id'],))
        holder.rollback()


@allure.title('Конкурентность: двое покупают последний товар — заказ получает только один')
def test_last_item_race(make_product, api, db, cache):
    product = make_product(stock=1)
    buyers = []
    for _ in range(2):
        from clients.api import ShopApi
        client = ShopApi(settings.BASE_URL)
        email = f'race-{uuid.uuid4().hex}@example.test'
        client.register(email, 'Study-password-123')
        client.login(email, 'Study-password-123')
        client.put_cart(product['id'], 1)
        buyers.append(client)
    statuses = []

    def checkout(client):
        statuses.append(client.create_order('Самара, Учебная улица, 10').status_code)

    try:
        threads = [threading.Thread(target=checkout, args=(client,)) for client in buyers]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert sorted(statuses) == [201, 409]
        assert db.scalar('SELECT stock FROM products WHERE id=%s', (product['id'],)) == 0
    finally:
        for client in buyers:
            cache.delete_user_data(client.user['id'])
            db.execute('DELETE FROM users WHERE id=%s', (client.user['id'],))
            client.close()


@allure.title('ON DELETE CASCADE: удаление пользователя удаляет его заказы и позиции')
def test_cascade_delete(db, user, order):
    with db.transaction() as connection:
        connection.execute('DELETE FROM users WHERE id=%s', (user.user['id'],))
        orders = connection.execute('SELECT COUNT(*) FROM orders WHERE id=%s', (order['id'],)).fetchone()
        items = connection.execute('SELECT COUNT(*) FROM order_items WHERE order_id=%s', (order['id'],)).fetchone()
        # Откатываем удаление: пользователь ещё нужен fixture для очистки.
        raise psycopg.Rollback()

    assert (orders['count'], items['count']) == (0, 0)


@allure.title('Схема: какие ограничения объявлены на таблице products')
def test_schema_from_catalog(db):
    checks = db.all(
        """
        SELECT pg_get_constraintdef(c.oid) AS definition
        FROM pg_constraint c JOIN pg_class t ON t.oid = c.conrelid
        WHERE t.relname = 'products' AND c.contype = 'c'
        ORDER BY 1
        """
    )

    assert [row['definition'] for row in checks] == ['CHECK ((price > 0))', 'CHECK ((stock >= 0))']
