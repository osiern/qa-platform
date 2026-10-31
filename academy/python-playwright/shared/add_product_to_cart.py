import allure
from playwright.sync_api import expect

from pages.shop_page import ShopPage


def add_product_to_cart(shop: ShopPage, world: dict) -> None:
    """Добавление первого товара сценария в корзину и переход в неё."""
    with allure.step('it: Нажать «В корзину» у своего товара'):
        shop.add_to_cart(world['product']['id'])

    with allure.step('check: Магазин подтвердил добавление'):
        expect(shop.message).to_have_text('Товар добавлен')

    with allure.step('it: Открыть корзину'):
        shop.open_cart()

    with allure.step('check: Товар отображается в корзине'):
        expect(shop.cart_row(world['product']['id'])).to_be_visible()
