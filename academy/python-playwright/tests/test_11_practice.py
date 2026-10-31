import allure
import pytest
from playwright.sync_api import expect

# project: QA Market
# description: academy/docs/LESSON-01.md
# prio: Blocker
# casegroup: Заказы
# team: Academy
# env: local

# Упражнение. Удали декоратор skip и замени каждый raise на одно действие или одну проверку.
# Вход и корзину пиши шагами вручную, без shared/login.py — это и есть практика.

@pytest.mark.skip(reason='Заполни TODO и удали этот декоратор')
def test_practice(shop, world):
    DATA = {'address': 'Самара, Учебная улица, 10'}
    with allure.step('pre: Открыть магазин'):
        shop.open()
    with allure.step('it: Ввести email'):
        # TODO: Ввести email
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('it: Ввести пароль'):
        # TODO: Ввести пароль
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('it: Нажать «Войти»'):
        # TODO: Нажать «Войти»
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('it: Ввести название товара в поиск'):
        # TODO: Ввести название товара в поиск
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('it: Нажать «Найти»'):
        # TODO: Нажать «Найти»
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('it: Добавить товар в корзину'):
        # TODO: Добавить товар в корзину
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('check: Магазин подтвердил добавление товара'):
        # TODO: Магазин подтвердил добавление товара
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('it: Открыть корзину'):
        # TODO: Открыть корзину
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('check: Сумма корзины равна цене товара'):
        # TODO: Сумма корзины равна цене товара
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('it: Ввести адрес доставки'):
        # TODO: Ввести адрес доставки
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('it: Оформить заказ'):
        # TODO: Оформить заказ
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('check: Заказ имеет статус new'):
        # TODO: Заказ имеет статус new
        raise NotImplementedError('Выполни шаг упражнения')
    with allure.step('check: Сумма заказа равна цене товара'):
        # TODO: Сумма заказа равна цене товара
        raise NotImplementedError('Выполни шаг упражнения')
