from contextlib import contextmanager

import allure
import psycopg
from psycopg.rows import dict_row


class Db:
    """Чтение и запись PostgreSQL напрямую.

    Параметры всегда передаются отдельно от текста запроса (%s),
    никогда через f-строку: так драйвер экранирует значения и SQL-инъекция невозможна.
    """

    def __init__(self, url: str):
        self.url = url
        # autocommit: каждый запрос — отдельная транзакция, тест видит данные, которые только что записал API.
        self.connection = psycopg.connect(url, autocommit=True, row_factory=dict_row)

    def close(self) -> None:
        self.connection.close()

    def all(self, sql: str, params: tuple = ()) -> list[dict]:
        with allure.step(f'SQL: {_short(sql)}'):
            allure.attach(f'{sql}\n-- params: {params}', name='sql', attachment_type=allure.attachment_type.TEXT)
            return self.connection.execute(sql, params).fetchall()

    def one(self, sql: str, params: tuple = ()) -> dict | None:
        rows = self.all(sql, params)
        assert len(rows) <= 1, f'Ожидалась одна строка, получено {len(rows)}'
        return rows[0] if rows else None

    def scalar(self, sql: str, params: tuple = ()):
        row = self.one(sql, params)
        return None if row is None else next(iter(row.values()))

    def execute(self, sql: str, params: tuple = ()) -> int:
        with allure.step(f'SQL: {_short(sql)}'):
            return self.connection.execute(sql, params).rowcount

    @contextmanager
    def transaction(self):
        """Отдельное соединение с явной транзакцией: BEGIN ... COMMIT или ROLLBACK при ошибке."""
        with psycopg.connect(self.url, row_factory=dict_row) as connection:
            with connection.transaction():
                yield connection


def _short(sql: str) -> str:
    return ' '.join(sql.split())[:90]
