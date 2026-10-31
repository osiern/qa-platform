import allure
import pytest
from playwright.sync_api import expect

from shared.open_shop import open_shop
from shared.search_own_products import search_own_products

# project: QA Market
# description: academy/docs/CASES.md#03
# prio: Normal
# casegroup: Каталог
# team: Academy
# env: local


# Цены товаров: 1234, 1334 и 1434 ₽. Диапазон — от первой до второй цены.
@allure.title('Каталог: обе границы диапазона цен включены в фильтр')
@pytest.mark.parametrize('product_count', [3], indirect=True)
def test_03(shop, world):
    products = world['products']
    in_range = [products[0]['id'], products[1]['id']]

    open_shop(shop)
    search_own_products(shop, world, all_products=True)

    with allure.step('it: Ввести «Цена от» равной цене первого товара'):
        shop.enter_min_price(products[0]['price'] / 100)

    with allure.step('it: Ввести «Цена до» равной цене второго товара'):
        shop.enter_max_price(products[1]['price'] / 100)

    with allure.step('it: Нажать «Найти»'):
        shop.submit_search()

    with allure.step('auto: Дождаться отфильтрованной выдачи'):
        shop.wait_for_product_ids(in_range)

    with allure.step('check: В выдаче оба товара на границах и нет товара за верхней границей'):
        assert shop.product_ids() == in_range

    with allure.step('check: Счётчик показывает два товара'):
        expect(shop.catalog_count).to_have_attribute('data-count', '2')
