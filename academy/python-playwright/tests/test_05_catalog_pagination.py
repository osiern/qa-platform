import allure
import pytest
from playwright.sync_api import expect

from shared.open_shop import open_shop
from shared.search_own_products import search_own_products

# project: QA Market
# description: academy/docs/CASES.md#05
# prio: Normal
# casegroup: Каталог
# team: Academy
# env: local


# 4 товара при 3 на странице: полная первая страница и неполная последняя.
@allure.title('Каталог: переход между страницами без дублей и пропусков')
@pytest.mark.parametrize('product_count', [4], indirect=True)
def test_05(shop, world):
    DATA = {'page_size': 3}
    products = world['products']
    first_page = [product['id'] for product in products[:DATA['page_size']]]

    open_shop(shop)
    search_own_products(shop, world, all_products=True)

    with allure.step(f"it: Выбрать «Товаров на странице: {DATA['page_size']}»"):
        shop.select_page_size(DATA['page_size'])

    with allure.step('auto: Дождаться первой страницы'):
        shop.wait_for_product_ids(first_page)

    with allure.step('check: На первой странице кнопка «Назад» недоступна'):
        expect(shop.previous_page_button).to_be_disabled()

    with allure.step('it: Нажать «Далее»'):
        shop.next_page()

    with allure.step('auto: Дождаться второй страницы'):
        shop.wait_for_product_ids([products[3]['id']])

    with allure.step('check: На второй странице только четвёртый товар'):
        assert shop.product_ids() == [products[3]['id']]

    with allure.step('check: На последней странице кнопка «Далее» недоступна'):
        expect(shop.next_page_button).to_be_disabled()

    with allure.step('it: Нажать «Назад»'):
        shop.previous_page()

    with allure.step('auto: Дождаться первой страницы повторно'):
        shop.wait_for_product_ids(first_page)

    with allure.step('check: Отображается «Страница 1 из 2»'):
        expect(shop.page_info).to_have_text('Страница 1 из 2')
