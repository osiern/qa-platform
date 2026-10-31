import allure
from playwright.sync_api import expect

from shared.add_product_to_cart import add_product_to_cart
from shared.login import login
from shared.open_shop import open_shop
from shared.search_own_products import search_own_products

# project: QA Market
# description: academy/docs/CASES.md#08
# prio: Critical
# casegroup: Заказы
# team: Academy
# env: local


@allure.title('Заказы: адрес короче 5 символов не создаёт заказ')
def test_08(shop, world):
    # Граница поля — 5–300 символов. 4 — ближайшее недопустимое значение.
    DATA = {
        'address': '1234',
        'error': 'Укажите адрес: от 5 до 300 символов',
    }

    open_shop(shop)
    login(shop, world)
    search_own_products(shop, world)
    add_product_to_cart(shop, world)

    with allure.step('it: Ввести адрес из 4 символов'):
        shop.enter_address(DATA['address'])

    with allure.step('it: Нажать «Оформить заказ»'):
        shop.submit_order()

    with allure.step('check: Показана ошибка длины адреса'):
        expect(shop.address_error).to_have_text(DATA['error'])

    with allure.step('check: Поле адреса отмечено aria-invalid'):
        expect(shop.address_input).to_have_attribute('aria-invalid', 'true')

    with allure.step('check: Товар остался в корзине'):
        expect(shop.cart_row(world['product']['id'])).to_be_visible()

    with allure.step('it: Открыть заказы'):
        shop.open_orders()

    with allure.step('check: Заказ не создан'):
        expect(shop.empty_orders).to_be_visible()
