import { expect, type Page, type Locator } from '@playwright/test';

export class ShopPage {
    constructor(readonly page: Page) {}

    // Общие элементы и авторизация
    get readyBody(): Locator {
        return this.page.locator('body[data-ready="true"]');
    }
    get message(): Locator {
        return this.page.getByRole('status');
    }
    get authPanel(): Locator {
        return this.page.locator('#auth');
    }
    get emailInput(): Locator {
        return this.page.getByLabel('Email', { exact: true });
    }
    get passwordInput(): Locator {
        return this.page.getByLabel('Пароль', { exact: true });
    }
    get showPasswordCheckbox(): Locator {
        return this.page.getByLabel('Показать пароль', { exact: true });
    }
    get loginButton(): Locator {
        return this.page.getByRole('button', { name: 'Войти', exact: true });
    }
    get registerButton(): Locator {
        return this.page.getByRole('button', { name: 'Зарегистрироваться', exact: true });
    }
    get logoutButton(): Locator {
        return this.page.getByRole('button', { name: 'Выйти', exact: true });
    }
    get identity(): Locator {
        return this.page.getByTestId('identity-email');
    }

    // Навигация
    get catalogButton(): Locator {
        return this.page.getByRole('button', { name: 'Каталог', exact: true });
    }
    get cartButton(): Locator {
        return this.page.getByRole('button', { name: 'Корзина', exact: true });
    }
    get ordersButton(): Locator {
        return this.page.getByRole('button', { name: 'Заказы', exact: true });
    }
    get profileButton(): Locator {
        return this.page.getByRole('button', { name: 'Профиль', exact: true });
    }

    // Каталог, фильтры и страницы
    get searchInput(): Locator {
        return this.page.getByLabel('Поиск', { exact: true });
    }
    get categorySelect(): Locator {
        return this.page.getByLabel('Категория', { exact: true });
    }
    get sortSelect(): Locator {
        return this.page.getByLabel('Сортировка', { exact: true });
    }
    get minPriceInput(): Locator {
        return this.page.getByLabel('Цена от, ₽', { exact: true });
    }
    get maxPriceInput(): Locator {
        return this.page.getByLabel('Цена до, ₽', { exact: true });
    }
    get inStockCheckbox(): Locator {
        return this.page.getByLabel('Только в наличии', { exact: true });
    }
    get favoritesOnlyCheckbox(): Locator {
        return this.page.getByLabel('Только избранное', { exact: true });
    }
    get findButton(): Locator {
        return this.page.getByRole('button', { name: 'Найти', exact: true });
    }
    get resetFiltersButton(): Locator {
        return this.page.getByRole('button', { name: 'Сбросить фильтры', exact: true });
    }
    get filterError(): Locator {
        return this.page.locator('#filter-error');
    }
    get catalogCount(): Locator {
        return this.page.getByTestId('result-count');
    }
    get pageSizeSelect(): Locator {
        return this.page.getByLabel('Товаров на странице');
    }
    get previousPageButton(): Locator {
        return this.page.getByRole('button', { name: 'Назад', exact: true });
    }
    get nextPageButton(): Locator {
        return this.page.getByRole('button', { name: 'Далее', exact: true });
    }
    get pageInfo(): Locator {
        return this.page.getByTestId('page-info');
    }
    get emptyCatalog(): Locator {
        return this.page.getByTestId('empty-catalog');
    }
    get cards(): Locator {
        return this.page.getByTestId('product-card');
    }

    // Окно товара
    get detailsDialog(): Locator {
        return this.page.locator('#details');
    }
    get detailsImage(): Locator {
        return this.page.locator('#details-image');
    }
    get detailsName(): Locator {
        return this.page.locator('#details-name');
    }
    get detailsDescription(): Locator {
        return this.page.locator('#details-description');
    }
    get detailsPrice(): Locator {
        return this.page.locator('#details-price');
    }
    get closeDetailsButton(): Locator {
        return this.page.getByRole('button', { name: 'Закрыть', exact: true });
    }

    // Корзина и оформление
    get cartTotal(): Locator {
        return this.page.getByTestId('cart-total');
    }
    get emptyCart(): Locator {
        return this.page.getByTestId('empty-cart');
    }
    get couponInput(): Locator {
        return this.page.getByLabel('Промокод', { exact: true });
    }
    get applyCouponButton(): Locator {
        return this.page.getByRole('button', { name: 'Применить промокод', exact: true });
    }
    get discountTotal(): Locator {
        return this.page.getByTestId('discount-total');
    }
    get addressInput(): Locator {
        return this.page.getByLabel('Адрес доставки', { exact: true });
    }
    get addressError(): Locator {
        return this.page.locator('#address-error');
    }
    get checkoutButton(): Locator {
        return this.page.getByRole('button', { name: 'Оформить заказ', exact: true });
    }

    // Заказы и подтверждение отмены
    get orderFilterSelect(): Locator {
        return this.page.getByLabel('Статус заказа');
    }
    get refreshOrdersButton(): Locator {
        return this.page.getByRole('button', { name: 'Обновить заказы', exact: true });
    }
    get emptyOrders(): Locator {
        return this.page.getByTestId('empty-orders');
    }
    get emptyFilteredOrders(): Locator {
        return this.page.getByTestId('empty-filtered-orders');
    }
    get orderCard(): Locator {
        return this.page.getByTestId('order-card');
    }
    get orderStatus(): Locator {
        return this.page.getByTestId('order-status');
    }
    get orderTotal(): Locator {
        return this.page.getByTestId('order-total');
    }
    get cancelDialog(): Locator {
        return this.page.locator('#cancel-dialog');
    }
    get keepOrderButton(): Locator {
        return this.page.getByRole('button', { name: 'Оставить заказ', exact: true });
    }
    get confirmCancelButton(): Locator {
        return this.page.getByRole('button', { name: 'Да, отменить', exact: true });
    }

    // Профиль
    get profileEmail(): Locator {
        return this.page.getByTestId('profile-email');
    }
    get profileNameInput(): Locator {
        return this.page.getByLabel('Имя', { exact: true });
    }
    get profileError(): Locator {
        return this.page.locator('#profile-error');
    }
    get saveProfileButton(): Locator {
        return this.page.getByRole('button', { name: 'Сохранить профиль', exact: true });
    }

    // Элементы конкретного товара, строки корзины и заказа
    product(id: number): Locator {
        return this.page.locator(`[data-testid="product-card"][data-id="${id}"]`);
    }
    cartRow(id: number): Locator {
        return this.page.locator(`[data-testid="cart-row"][data-id="${id}"]`);
    }
    orderById(id: number): Locator {
        return this.page.locator(`[data-testid="order-card"][data-id="${id}"]`);
    }
    productName(id: number): Locator {
        return this.product(id).getByRole('heading');
    }
    productImage(id: number): Locator {
        return this.product(id).getByRole('img');
    }
    productStock(id: number): Locator {
        return this.product(id).getByTestId('product-stock');
    }
    productDetailsButton(id: number): Locator {
        return this.product(id).getByRole('button', { name: 'Подробнее', exact: true });
    }
    addToCartButton(id: number): Locator {
        return this.product(id).getByRole('button', { name: 'В корзину', exact: true });
    }
    addFavoriteButton(id: number): Locator {
        return this.product(id).getByRole('button', { name: 'В избранное', exact: true });
    }
    removeFavoriteButton(id: number): Locator {
        return this.product(id).getByRole('button', { name: 'Убрать из избранного', exact: true });
    }
    quantityInput(id: number): Locator {
        return this.cartRow(id).getByRole('spinbutton');
    }
    removeFromCartButton(id: number): Locator {
        return this.cartRow(id).getByRole('button', { name: 'Удалить', exact: true });
    }
    orderStatusFor(id: number): Locator {
        return this.orderById(id).getByTestId('order-status');
    }
    orderTotalFor(id: number): Locator {
        return this.orderById(id).getByTestId('order-total');
    }
    cancelOrderButton(orderId?: number): Locator {
        return (orderId === undefined ? this.orderCard : this.orderById(orderId)).getByRole(
            'button',
            { name: 'Отменить заказ', exact: true },
        );
    }
    payOrderButton(orderId?: number): Locator {
        return (orderId === undefined ? this.orderCard : this.orderById(orderId)).getByRole(
            'button',
            { name: 'Оплатить', exact: true },
        );
    }

    // Действия: один метод — одно логическое действие
    async enterEmail(email: string) {
        await this.emailInput.fill(email);
    }
    async enterPassword(password: string) {
        await this.passwordInput.fill(password);
    }
    async enterSearch(name: string) {
        await this.searchInput.fill(name);
    }
    async enterMinPrice(price: number) {
        await this.minPriceInput.fill(String(price));
    }
    async enterMaxPrice(price: number) {
        await this.maxPriceInput.fill(String(price));
    }
    async enterCoupon(code: string) {
        await this.couponInput.fill(code);
    }
    async enterAddress(address: string) {
        await this.addressInput.fill(address);
    }
    async enterProfileName(name: string) {
        await this.profileNameInput.fill(name);
    }
    async submitLogin() {
        await this.loginButton.click();
    }
    async register() {
        await this.registerButton.click();
    }
    async submitSearch() {
        await this.findButton.click();
    }
    async openCatalog() {
        await this.catalogButton.click();
    }
    async openProfile() {
        await this.profileButton.click();
    }
    async openCart() {
        await this.cartButton.click();
    }
    async openOrders() {
        await this.ordersButton.click();
    }
    async nextPage() {
        await this.nextPageButton.click();
    }
    async previousPage() {
        await this.previousPageButton.click();
    }
    async resetFilters() {
        await this.resetFiltersButton.click();
    }
    async closeProductDetails() {
        await this.closeDetailsButton.click();
    }
    async applyCoupon() {
        await this.applyCouponButton.click();
    }
    async submitOrder() {
        await this.checkoutButton.click();
    }
    async keepOrder() {
        await this.keepOrderButton.click();
    }
    async confirmCancellation() {
        await this.confirmCancelButton.click();
    }
    async refreshOrders() {
        await this.refreshOrdersButton.click();
    }
    async saveProfile() {
        await this.saveProfileButton.click();
    }
    async addToCart(id: number) {
        await this.addToCartButton(id).click();
    }
    async removeFromCart(id: number) {
        await this.removeFromCartButton(id).click();
    }
    async openProductDetails(id: number) {
        await this.productDetailsButton(id).click();
    }
    async addToFavorites(id: number) {
        await this.addFavoriteButton(id).click();
    }
    async removeFromFavorites(id: number) {
        await this.removeFavoriteButton(id).click();
    }
    async requestCancellation(orderId?: number) {
        await this.cancelOrderButton(orderId).click();
    }
    async payOrder(orderId?: number) {
        await this.payOrderButton(orderId).click();
    }
    async selectCategory(value: string) {
        await this.categorySelect.selectOption(String(value));
    }
    async selectPageSize(value: number) {
        await this.pageSizeSelect.selectOption(String(value));
    }
    async filterOrdersByStatus(value: string) {
        await this.orderFilterSelect.selectOption(String(value));
    }
    async sortProductsByPriceAscending() {
        await this.sortSelect.selectOption('price_asc');
    }
    async sortProductsByPriceDescending() {
        await this.sortSelect.selectOption('price_desc');
    }
    async setOnlyInStock(enabled: boolean) {
        await this.inStockCheckbox.setChecked(enabled);
    }
    async setOnlyFavorites(enabled: boolean) {
        await this.favoritesOnlyCheckbox.setChecked(enabled);
    }
    async setPasswordVisible(enabled: boolean) {
        await this.showPasswordCheckbox.setChecked(enabled);
    }

    async open() {
        await this.page.goto('/');
        await this.readyBody.waitFor({ state: 'attached' });
    }
    async refresh() {
        await this.page.reload();
        await this.readyBody.waitFor({ state: 'attached' });
    }
    async logout() {
        await this.logoutButton.click();
        await this.emailInput.waitFor({ state: 'visible' });
    }
    async closeProductDetailsWithEscape() {
        await this.detailsDialog.press('Escape');
    }
    async changeQuantity(id: number, quantity: number) {
        await this.quantityInput(id).fill(String(quantity));
        await this.quantityInput(id).press('Tab');
    }
    async productCount(): Promise<number> {
        return this.cards.count();
    }
    async productIds(): Promise<number[]> {
        // Снимок всех атрибутов за одно чтение: каталог может перерисовываться.
        return this.cards.evaluateAll((cards) =>
            cards.map((card) => Number(card.getAttribute('data-id'))),
        );
    }
    async productPrices(): Promise<number[]> {
        return this.cards.evaluateAll((cards) =>
            cards.map((card) => Number(card.getAttribute('data-price'))),
        );
    }
    async waitForProductIds(ids: number[]) {
        await expect.poll(() => this.productIds()).toEqual(ids);
    }
    async waitForOrderStatus(status: string) {
        // Оплата асинхронная: перезапрашиваем список, пока worker не обработает событие.
        await expect(async () => {
            await this.refreshOrders();
            await expect(this.orderStatus).toHaveText(status, { timeout: 1000 });
        }).toPass({ timeout: 20000, intervals: [500] });
    }
}
