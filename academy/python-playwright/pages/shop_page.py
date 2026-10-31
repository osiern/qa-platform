import time

from playwright.sync_api import Locator, Page, expect


class ShopPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    # Общие элементы и авторизация
    @property
    def ready_body(self) -> Locator:
        return self.page.locator('body[data-ready="true"]')

    @property
    def message(self) -> Locator:
        return self.page.get_by_role('status')

    @property
    def auth_panel(self) -> Locator:
        return self.page.locator('#auth')

    @property
    def email_input(self) -> Locator:
        return self.page.get_by_label('Email', exact=True)

    @property
    def password_input(self) -> Locator:
        return self.page.get_by_label('Пароль', exact=True)

    @property
    def show_password_checkbox(self) -> Locator:
        return self.page.get_by_label('Показать пароль', exact=True)

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_role('button', name='Войти', exact=True)

    @property
    def register_button(self) -> Locator:
        return self.page.get_by_role('button', name='Зарегистрироваться', exact=True)

    @property
    def logout_button(self) -> Locator:
        return self.page.get_by_role('button', name='Выйти', exact=True)

    @property
    def identity(self) -> Locator:
        return self.page.get_by_test_id('identity-email')


    # Навигация
    @property
    def catalog_button(self) -> Locator:
        return self.page.get_by_role('button', name='Каталог', exact=True)

    @property
    def cart_button(self) -> Locator:
        return self.page.get_by_role('button', name='Корзина', exact=True)

    @property
    def orders_button(self) -> Locator:
        return self.page.get_by_role('button', name='Заказы', exact=True)

    @property
    def profile_button(self) -> Locator:
        return self.page.get_by_role('button', name='Профиль', exact=True)


    # Каталог, фильтры и страницы
    @property
    def search_input(self) -> Locator:
        return self.page.get_by_label('Поиск', exact=True)

    @property
    def category_select(self) -> Locator:
        return self.page.get_by_label('Категория', exact=True)

    @property
    def sort_select(self) -> Locator:
        return self.page.get_by_label('Сортировка', exact=True)

    @property
    def min_price_input(self) -> Locator:
        return self.page.get_by_label('Цена от, ₽', exact=True)

    @property
    def max_price_input(self) -> Locator:
        return self.page.get_by_label('Цена до, ₽', exact=True)

    @property
    def in_stock_checkbox(self) -> Locator:
        return self.page.get_by_label('Только в наличии', exact=True)

    @property
    def favorites_only_checkbox(self) -> Locator:
        return self.page.get_by_label('Только избранное', exact=True)

    @property
    def find_button(self) -> Locator:
        return self.page.get_by_role('button', name='Найти', exact=True)

    @property
    def reset_filters_button(self) -> Locator:
        return self.page.get_by_role('button', name='Сбросить фильтры', exact=True)

    @property
    def filter_error(self) -> Locator:
        return self.page.locator('#filter-error')

    @property
    def catalog_count(self) -> Locator:
        return self.page.get_by_test_id('result-count')

    @property
    def page_size_select(self) -> Locator:
        return self.page.get_by_label('Товаров на странице')

    @property
    def previous_page_button(self) -> Locator:
        return self.page.get_by_role('button', name='Назад', exact=True)

    @property
    def next_page_button(self) -> Locator:
        return self.page.get_by_role('button', name='Далее', exact=True)

    @property
    def page_info(self) -> Locator:
        return self.page.get_by_test_id('page-info')

    @property
    def empty_catalog(self) -> Locator:
        return self.page.get_by_test_id('empty-catalog')

    @property
    def cards(self) -> Locator:
        return self.page.get_by_test_id('product-card')


    # Окно товара
    @property
    def details_dialog(self) -> Locator:
        return self.page.locator('#details')

    @property
    def details_image(self) -> Locator:
        return self.page.locator('#details-image')

    @property
    def details_name(self) -> Locator:
        return self.page.locator('#details-name')

    @property
    def details_description(self) -> Locator:
        return self.page.locator('#details-description')

    @property
    def details_price(self) -> Locator:
        return self.page.locator('#details-price')

    @property
    def close_details_button(self) -> Locator:
        return self.page.get_by_role('button', name='Закрыть', exact=True)


    # Корзина и оформление
    @property
    def cart_total(self) -> Locator:
        return self.page.get_by_test_id('cart-total')

    @property
    def empty_cart(self) -> Locator:
        return self.page.get_by_test_id('empty-cart')

    @property
    def coupon_input(self) -> Locator:
        return self.page.get_by_label('Промокод', exact=True)

    @property
    def apply_coupon_button(self) -> Locator:
        return self.page.get_by_role('button', name='Применить промокод', exact=True)

    @property
    def discount_total(self) -> Locator:
        return self.page.get_by_test_id('discount-total')

    @property
    def address_input(self) -> Locator:
        return self.page.get_by_label('Адрес доставки', exact=True)

    @property
    def address_error(self) -> Locator:
        return self.page.locator('#address-error')

    @property
    def checkout_button(self) -> Locator:
        return self.page.get_by_role('button', name='Оформить заказ', exact=True)


    # Заказы и подтверждение отмены
    @property
    def order_filter_select(self) -> Locator:
        return self.page.get_by_label('Статус заказа')

    @property
    def refresh_orders_button(self) -> Locator:
        return self.page.get_by_role('button', name='Обновить заказы', exact=True)

    @property
    def empty_orders(self) -> Locator:
        return self.page.get_by_test_id('empty-orders')

    @property
    def empty_filtered_orders(self) -> Locator:
        return self.page.get_by_test_id('empty-filtered-orders')

    @property
    def order_card(self) -> Locator:
        return self.page.get_by_test_id('order-card')

    @property
    def order_status(self) -> Locator:
        return self.page.get_by_test_id('order-status')

    @property
    def order_total(self) -> Locator:
        return self.page.get_by_test_id('order-total')

    @property
    def cancel_dialog(self) -> Locator:
        return self.page.locator('#cancel-dialog')

    @property
    def keep_order_button(self) -> Locator:
        return self.page.get_by_role('button', name='Оставить заказ', exact=True)

    @property
    def confirm_cancel_button(self) -> Locator:
        return self.page.get_by_role('button', name='Да, отменить', exact=True)


    # Профиль
    @property
    def profile_email(self) -> Locator:
        return self.page.get_by_test_id('profile-email')

    @property
    def profile_name_input(self) -> Locator:
        return self.page.get_by_label('Имя', exact=True)

    @property
    def profile_error(self) -> Locator:
        return self.page.locator('#profile-error')

    @property
    def save_profile_button(self) -> Locator:
        return self.page.get_by_role('button', name='Сохранить профиль', exact=True)


    # Элементы конкретного товара, строки корзины и заказа
    def product(self, entity_id: int) -> Locator:
        return self.page.locator(f'[data-testid="product-card"][data-id="{entity_id}"]')

    def cart_row(self, entity_id: int) -> Locator:
        return self.page.locator(f'[data-testid="cart-row"][data-id="{entity_id}"]')

    def order_by_id(self, entity_id: int) -> Locator:
        return self.page.locator(f'[data-testid="order-card"][data-id="{entity_id}"]')

    def product_name(self, entity_id: int) -> Locator:
        return self.product(entity_id).get_by_role('heading')

    def product_image(self, entity_id: int) -> Locator:
        return self.product(entity_id).get_by_role('img')

    def product_stock(self, entity_id: int) -> Locator:
        return self.product(entity_id).get_by_test_id('product-stock')

    def product_details_button(self, entity_id: int) -> Locator:
        return self.product(entity_id).get_by_role('button', name='Подробнее', exact=True)

    def add_to_cart_button(self, entity_id: int) -> Locator:
        return self.product(entity_id).get_by_role('button', name='В корзину', exact=True)

    def add_favorite_button(self, entity_id: int) -> Locator:
        return self.product(entity_id).get_by_role('button', name='В избранное', exact=True)

    def remove_favorite_button(self, entity_id: int) -> Locator:
        return self.product(entity_id).get_by_role('button', name='Убрать из избранного', exact=True)

    def quantity_input(self, entity_id: int) -> Locator:
        return self.cart_row(entity_id).get_by_role('spinbutton')

    def remove_from_cart_button(self, entity_id: int) -> Locator:
        return self.cart_row(entity_id).get_by_role('button', name='Удалить', exact=True)

    def order_status_for(self, entity_id: int) -> Locator:
        return self.order_by_id(entity_id).get_by_test_id('order-status')

    def order_total_for(self, entity_id: int) -> Locator:
        return self.order_by_id(entity_id).get_by_test_id('order-total')

    def cancel_order_button(self, order_id: int | None = None) -> Locator:
        order = self.order_card if order_id is None else self.order_by_id(order_id)
        return order.get_by_role('button', name='Отменить заказ', exact=True)

    def pay_order_button(self, order_id: int | None = None) -> Locator:
        order = self.order_card if order_id is None else self.order_by_id(order_id)
        return order.get_by_role('button', name='Оплатить', exact=True)


    # Действия: один метод — одно логическое действие
    def enter_email(self, email: str) -> None:
        self.email_input.fill(email)

    def enter_password(self, password: str) -> None:
        self.password_input.fill(password)

    def enter_search(self, name: str) -> None:
        self.search_input.fill(name)

    def enter_min_price(self, price: float) -> None:
        self.min_price_input.fill(str(price))

    def enter_max_price(self, price: float) -> None:
        self.max_price_input.fill(str(price))

    def enter_coupon(self, code: str) -> None:
        self.coupon_input.fill(code)

    def enter_address(self, address: str) -> None:
        self.address_input.fill(address)

    def enter_profile_name(self, name: str) -> None:
        self.profile_name_input.fill(name)

    def submit_login(self) -> None:
        self.login_button.click()

    def register(self) -> None:
        self.register_button.click()

    def submit_search(self) -> None:
        self.find_button.click()

    def open_catalog(self) -> None:
        self.catalog_button.click()

    def open_profile(self) -> None:
        self.profile_button.click()

    def open_cart(self) -> None:
        self.cart_button.click()

    def open_orders(self) -> None:
        self.orders_button.click()

    def next_page(self) -> None:
        self.next_page_button.click()

    def previous_page(self) -> None:
        self.previous_page_button.click()

    def reset_filters(self) -> None:
        self.reset_filters_button.click()

    def close_product_details(self) -> None:
        self.close_details_button.click()

    def apply_coupon(self) -> None:
        self.apply_coupon_button.click()

    def submit_order(self) -> None:
        self.checkout_button.click()

    def keep_order(self) -> None:
        self.keep_order_button.click()

    def confirm_cancellation(self) -> None:
        self.confirm_cancel_button.click()

    def refresh_orders(self) -> None:
        self.refresh_orders_button.click()

    def save_profile(self) -> None:
        self.save_profile_button.click()

    def add_to_cart(self, product_id: int) -> None:
        self.add_to_cart_button(product_id).click()

    def remove_from_cart(self, product_id: int) -> None:
        self.remove_from_cart_button(product_id).click()

    def open_product_details(self, product_id: int) -> None:
        self.product_details_button(product_id).click()

    def add_to_favorites(self, product_id: int) -> None:
        self.add_favorite_button(product_id).click()

    def remove_from_favorites(self, product_id: int) -> None:
        self.remove_favorite_button(product_id).click()

    def request_cancellation(self, order_id: int | None = None) -> None:
        self.cancel_order_button(order_id).click()

    def pay_order(self, order_id: int | None = None) -> None:
        self.pay_order_button(order_id).click()

    def select_category(self, value: str) -> None:
        self.category_select.select_option(str(value))

    def select_page_size(self, value: int) -> None:
        self.page_size_select.select_option(str(value))

    def filter_orders_by_status(self, value: str) -> None:
        self.order_filter_select.select_option(str(value))

    def sort_products_by_price_ascending(self) -> None:
        self.sort_select.select_option('price_asc')

    def sort_products_by_price_descending(self) -> None:
        self.sort_select.select_option('price_desc')

    def set_only_in_stock(self, enabled: bool) -> None:
        self.in_stock_checkbox.set_checked(enabled)

    def set_only_favorites(self, enabled: bool) -> None:
        self.favorites_only_checkbox.set_checked(enabled)

    def set_password_visible(self, enabled: bool) -> None:
        self.show_password_checkbox.set_checked(enabled)


    def open(self) -> None:
        self.page.goto(self.base_url)
        self.ready_body.wait_for(state='attached')

    def refresh(self) -> None:
        self.page.reload()
        self.ready_body.wait_for(state='attached')

    def logout(self) -> None:
        self.logout_button.click()
        self.email_input.wait_for(state='visible')

    def close_product_details_with_escape(self) -> None:
        self.details_dialog.press('Escape')

    def change_quantity(self, product_id: int, quantity: int) -> None:
        self.quantity_input(product_id).fill(str(quantity))
        self.quantity_input(product_id).press('Tab')

    def product_count(self) -> int:
        return self.cards.count()

    def product_ids(self) -> list[int]:
        # Один снимок атрибутов, без обращения к исчезающим индексам.
        return self.cards.evaluate_all("cards => cards.map(card => Number(card.getAttribute('data-id')))")

    def product_prices(self) -> list[int]:
        return self.cards.evaluate_all("cards => cards.map(card => Number(card.getAttribute('data-price')))")

    def wait_for_product_ids(self, ids: list[int]) -> None:
        # Техническое ожидание точного набора, бизнес-проверки остаются в тесте.
        expect(self.cards).to_have_count(len(ids))
        for index, product_id in enumerate(ids):
            expect(self.cards.nth(index)).to_have_attribute('data-id', str(product_id))

    def wait_for_order_status(self, status: str, timeout: float = 20) -> None:
        # Оплата асинхронная: перезапрашиваем список, пока worker не обработает событие.
        deadline = time.monotonic() + timeout
        while True:
            self.refresh_orders()
            try:
                expect(self.order_status).to_have_text(status, timeout=1000)
                return
            except AssertionError:
                if time.monotonic() > deadline:
                    raise
