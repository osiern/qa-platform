import allure
from playwright.sync_api import expect

from shared.add_product_to_cart import add_product_to_cart
from shared.login import login
from shared.open_shop import open_shop
from shared.search_own_products import search_own_products

# project: QA Market
# description: academy/docs/CASES.md#07
# prio: Critical
# casegroup: Корзина
# team: Academy
# env: local


# Остаток товара — 10 шт. Сервер отвечает 409 на количество 11.
@allure.title('Корзина: количество больше остатка отклоняется, корзина сохраняется')
def test_07(shop, world):
    DATA = {'quantity': 3}
    product = world['product']

    open_shop(shop)
    login(shop, world)
    search_own_products(shop, world)
    add_product_to_cart(shop, world)

    with allure.step(f"it: Изменить количество на {DATA['quantity']}"):
        shop.change_quantity(product['id'], DATA['quantity'])

    with allure.step('check: Корзина подтвердила изменение'):
        expect(shop.message).to_have_text('Количество обновлено')

    with allure.step(f"check: Сумма равна цене {DATA['quantity']} шт."):
        expect(shop.cart_total).to_have_attribute('data-cents', str(product['price'] * DATA['quantity']))

    with allure.step('it: Изменить количество на число больше остатка'):
        shop.change_quantity(product['id'], product['stock'] + 1)

    with allure.step('check: Показана ошибка «Недостаточно товара»'):
        expect(shop.message).to_have_text('Недостаточно товара')

    with allure.step(f"check: В поле вернулось сохранённое количество {DATA['quantity']}"):
        expect(shop.quantity_input(product['id'])).to_have_value(str(DATA['quantity']))

    with allure.step('it: Обновить страницу'):
        shop.refresh()

    with allure.step('it: Открыть корзину'):
        shop.open_cart()

    with allure.step(f"check: После обновления в корзине {DATA['quantity']} шт."):
        expect(shop.quantity_input(product['id'])).to_have_value(str(DATA['quantity']))
