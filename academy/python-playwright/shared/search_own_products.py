import allure

from pages.shop_page import ShopPage


def search_own_products(shop: ShopPage, world: dict, all_products: bool = False) -> None:
    """Поиск товаров сценария.

    all_products=False — только первый товар по точному названию,
    all_products=True — все товары по общему префиксу.
    """
    title = 'Ввести общий префикс своих товаров' if all_products else 'Ввести название своего товара'
    with allure.step(f'it: {title}'):
        shop.enter_search(world['searchPrefix'] if all_products else world['product']['name'])

    with allure.step('it: Нажать «Найти»'):
        shop.submit_search()

    with allure.step('auto: Дождаться результата поиска'):
        ids = [product['id'] for product in world['products']] if all_products else [world['product']['id']]
        shop.wait_for_product_ids(ids)
