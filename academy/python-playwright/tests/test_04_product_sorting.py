import allure
import pytest

from shared.open_shop import open_shop
from shared.search_own_products import search_own_products

# project: QA Market
# description: academy/docs/CASES.md#04
# prio: Normal
# casegroup: Каталог
# team: Academy
# env: local


@allure.title('Каталог: сортировка товаров по возрастанию цены')
@pytest.mark.parametrize('product_count', [3], indirect=True)
def test_04(shop, world):
    products = world['products']

    open_shop(shop)
    search_own_products(shop, world, all_products=True)

    # Без обратного порядка проверка «по возрастанию» прошла бы и без сортировки:
    # товары созданы в порядке роста цены.
    with allure.step('it: Выбрать сортировку «Сначала дороже»'):
        shop.sort_products_by_price_descending()

    with allure.step('auto: Дождаться обратного порядка'):
        shop.wait_for_product_ids([product['id'] for product in reversed(products)])

    with allure.step('it: Выбрать сортировку «Сначала дешевле»'):
        shop.sort_products_by_price_ascending()

    with allure.step('auto: Дождаться завершения сортировки'):
        shop.wait_for_product_ids([p['id'] for p in sorted(products, key=lambda p: p['price'])])

    with allure.step('check: Цены идут по возрастанию'):
        assert shop.product_prices() == sorted(product['price'] for product in products)
