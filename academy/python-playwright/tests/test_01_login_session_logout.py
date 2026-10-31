import allure
from playwright.sync_api import expect

from shared.login import login
from shared.open_shop import open_shop

# project: QA Market
# description: academy/docs/CASES.md#01
# prio: Critical
# casegroup: Авторизация
# team: Academy
# env: local


@allure.title('Авторизация: вход, сохранение сессии после обновления и выход')
def test_01(shop, world):
    open_shop(shop)
    login(shop, world)

    with allure.step('it: Открыть профиль'):
        shop.open_profile()

    with allure.step('check: В профиле отображается email пользователя'):
        expect(shop.profile_email).to_have_text(world['user']['email'])

    with allure.step('it: Обновить страницу'):
        shop.refresh()

    with allure.step('check: После обновления пользователь остаётся авторизован'):
        expect(shop.identity).to_have_text(world['user']['email'])

    with allure.step('it: Нажать «Выйти»'):
        shop.logout()

    with allure.step('check: Снова показана форма входа'):
        expect(shop.email_input).to_be_visible()

    with allure.step('check: Email исчез из шапки'):
        expect(shop.identity).to_have_count(0)
