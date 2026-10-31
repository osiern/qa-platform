import allure
from playwright.sync_api import expect

from shared.open_shop import open_shop

# project: QA Market
# description: academy/docs/CASES.md#02
# prio: Critical
# casegroup: Авторизация
# team: Academy
# env: local


@allure.title('Авторизация: неверный пароль не открывает аккаунт')
def test_02(shop, world):
    DATA = {
        'password': 'Wrong-password-123',
        'error': 'Неверный email или пароль',
    }

    open_shop(shop)

    with allure.step('it: Ввести email существующего пользователя'):
        shop.enter_email(world['user']['email'])

    with allure.step('it: Ввести неверный пароль'):
        shop.enter_password(DATA['password'])

    with allure.step('it: Нажать «Войти»'):
        shop.submit_login()

    with allure.step(f"check: Показана общая ошибка «{DATA['error']}»"):
        expect(shop.message).to_have_text(DATA['error'])

    with allure.step('check: Форма входа осталась открытой'):
        expect(shop.email_input).to_be_visible()

    with allure.step('check: Пользователь не авторизован'):
        expect(shop.identity).to_have_count(0)
