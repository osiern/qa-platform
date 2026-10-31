import allure
from playwright.sync_api import expect

from shared.add_product_to_cart import add_product_to_cart
from shared.login import login
from shared.open_shop import open_shop
from shared.place_order import place_order
from shared.search_own_products import search_own_products

# project: QA Market
# description: academy/docs/CASES.md#06
# prio: Blocker
# casegroup: Заказы
# team: Academy
# env: local



def discounted(price: int) -> str:
    # Деньги в копейках и целых числах: округление вниз, как на сервере.
    return str(price * 90 // 100)


@allure.title('Заказы: покупка со скидкой 10% по промокоду')
def test_06(shop, world):
    DATA = {
        'coupon': 'SAVE10',
        'address': 'Самара, Учебная улица, 10',
    }

    open_shop(shop)
    login(shop, world)
    search_own_products(shop, world)
    add_product_to_cart(shop, world)

    with allure.step(f"it: Ввести промокод «{DATA['coupon']}»"):
        shop.enter_coupon(DATA['coupon'])

    with allure.step('it: Нажать «Применить промокод»'):
        shop.apply_coupon()

    with allure.step('check: Сумма к оплате уменьшилась на 10%'):
        expect(shop.discount_total).to_have_attribute('data-cents', discounted(world['product']['price']))

    place_order(shop, DATA['address'])

    with allure.step('check: Сумма заказа совпадает с суммой со скидкой'):
        expect(shop.order_total).to_have_attribute('data-cents', discounted(world['product']['price']))

    with allure.step('it: Открыть корзину'):
        shop.open_cart()

    with allure.step('check: После покупки корзина пуста'):
        expect(shop.empty_cart).to_be_visible()
