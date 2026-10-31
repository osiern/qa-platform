import allure

from pages.shop_page import ShopPage


def open_shop(shop: ShopPage) -> None:
    """Шаг открытия магазина."""
    with allure.step('pre: Открыть магазин'):
        shop.open()
