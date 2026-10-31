import allure
from playwright.sync_api import expect

from shared.add_product_to_cart import add_product_to_cart
from shared.login import login
from shared.open_shop import open_shop
from shared.place_order import place_order
from shared.search_own_products import search_own_products

# project: QA Market
# description: academy/docs/CASES.md#10
# prio: Critical
# casegroup: Заказы
# team: Academy
# env: local


@allure.title('Заказы: отмена требует подтверждения и возвращает остаток')
def test_10(shop, world):
    DATA = {'address': 'Самара, Учебная улица, 10'}
    product = world['product']

    open_shop(shop)
    login(shop, world)
    search_own_products(shop, world)
    add_product_to_cart(shop, world)
    place_order(shop, DATA['address'])

    with allure.step('it: Открыть каталог'):
        shop.open_catalog()

    with allure.step('it: Нажать «Найти», чтобы перечитать остаток'):
        shop.submit_search()

    # Без этой проверки финальная «остаток вернулся» прошла бы и на старых данных.
    with allure.step('check: Остаток уменьшился на купленную единицу'):
        expect(shop.product_stock(product['id'])).to_have_text(f"В наличии: {product['stock'] - 1}")

    with allure.step('it: Открыть заказы'):
        shop.open_orders()

    with allure.step('it: Нажать «Отменить заказ»'):
        shop.request_cancellation()

    with allure.step('check: Открыто окно подтверждения'):
        expect(shop.cancel_dialog).to_be_visible()

    with allure.step('it: Нажать «Оставить заказ»'):
        shop.keep_order()

    with allure.step('check: Заказ сохранил статус new'):
        expect(shop.order_status).to_have_text('new')

    with allure.step('it: Снова нажать «Отменить заказ»'):
        shop.request_cancellation()

    with allure.step('it: Нажать «Да, отменить»'):
        shop.confirm_cancellation()

    with allure.step('check: Заказ получил статус cancelled'):
        expect(shop.order_status).to_have_text('cancelled')

    with allure.step('check: Окно подтверждения закрылось'):
        expect(shop.cancel_dialog).to_be_hidden()

    with allure.step('it: Открыть каталог'):
        shop.open_catalog()

    with allure.step('it: Нажать «Найти», чтобы перечитать остаток'):
        shop.submit_search()

    with allure.step('check: Остаток вернулся на склад'):
        expect(shop.product_stock(product['id'])).to_have_text(f"В наличии: {product['stock']}")
