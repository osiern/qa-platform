import allure
from playwright.sync_api import expect

from pages.shop_page import ShopPage


def login(shop: ShopPage, world: dict) -> None:
    """Вход через форму и проверка email в шапке."""
    with allure.step('it: Ввести email'):
        shop.enter_email(world['user']['email'])

    with allure.step('it: Ввести пароль'):
        shop.enter_password(world['user']['password'])

    with allure.step('it: Нажать «Войти»'):
        shop.submit_login()

    with allure.step('check: Email пользователя отображается в шапке'):
        expect(shop.identity).to_have_text(world['user']['email'])
