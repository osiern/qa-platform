import allure
from playwright.sync_api import expect

from shared.add_product_to_cart import add_product_to_cart
from shared.login import login
from shared.open_shop import open_shop
from shared.place_order import place_order
from shared.search_own_products import search_own_products

# project: QA Market
# description: academy/docs/CASES.md#09
# prio: Critical
# casegroup: Оплата
# team: Academy
# env: local


@allure.title('Оплата: асинхронная оплата переводит заказ в paid')
def test_09(shop, world):
    DATA = {'address': 'Самара, Учебная улица, 10'}

    open_shop(shop)
    login(shop, world)
    search_own_products(shop, world)
    add_product_to_cart(shop, world)
    place_order(shop, DATA['address'])

    with allure.step('it: Нажать «Оплатить»'):
        shop.pay_order()

    with allure.step('check: Магазин принял оплату в обработку'):
        expect(shop.message).to_have_text('Оплата передана в обработку')

    # Промежуточный payment_pending не проверяем: worker может успеть раньше.
    # Ждём конечное состояние, а не фиксированную паузу.
    with allure.step('auto: Обновлять список заказов, пока worker не обработает оплату'):
        shop.wait_for_order_status('paid')

    with allure.step('check: Заказ получил статус paid'):
        expect(shop.order_status).to_have_text('paid')

    with allure.step('check: Оплаченный заказ нельзя отменить'):
        expect(shop.cancel_order_button()).to_have_count(0)
