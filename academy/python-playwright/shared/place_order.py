import allure
from playwright.sync_api import expect

from pages.shop_page import ShopPage


def place_order(shop: ShopPage, address: str) -> None:
    """Оформление заказа из открытой корзины. Адрес — от 5 до 300 символов."""
    with allure.step('it: Ввести адрес доставки'):
        shop.enter_address(address)

    with allure.step('it: Нажать «Оформить заказ»'):
        shop.submit_order()

    with allure.step('check: Создан заказ со статусом new'):
        expect(shop.order_status).to_have_text('new')
