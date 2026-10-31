import { browser, $, $$ } from '@wdio/globals';
import { Key } from 'webdriverio';

// Как в рабочем проекте: один экземпляр на страницу.
// Элемент — геттер без скобок: Shop.emailInput.
// Элемент конкретной записи — метод: Shop.cartRow(id).
// Действие — async-метод: await Shop.enterEmail(value).
class ShopPage {
    // Общие элементы и авторизация
    get readyBody() {
        return $('body[data-ready="true"]');
    }
    get message() {
        return $('#status');
    }
    get authPanel() {
        return $('#auth');
    }
    get emailInput() {
        return $('[name="email"]');
    }
    get passwordInput() {
        return $('[name="password"]');
    }
    get showPasswordCheckbox() {
        return $('#show-password');
    }
    get loginButton() {
        return $('#auth-form button[type="submit"]');
    }
    get registerButton() {
        return $('#register');
    }
    get logoutButton() {
        return $('#identity button');
    }
    get identity() {
        return $('[data-testid="identity-email"]');
    }

    // Навигация
    get catalogButton() {
        return $('[data-view="catalog"]');
    }
    get cartButton() {
        return $('[data-view="cart"]');
    }
    get ordersButton() {
        return $('[data-view="orders"]');
    }
    get profileButton() {
        return $('[data-view="profile"]');
    }

    // Каталог, фильтры и страницы
    get searchInput() {
        return $('#search');
    }
    get categorySelect() {
        return $('#category');
    }
    get sortSelect() {
        return $('#sort');
    }
    get minPriceInput() {
        return $('#min-price');
    }
    get maxPriceInput() {
        return $('#max-price');
    }
    get inStockCheckbox() {
        return $('#in-stock');
    }
    get favoritesOnlyCheckbox() {
        return $('#only-favorites');
    }
    get findButton() {
        return $('#find');
    }
    get resetFiltersButton() {
        return $('#reset-filters');
    }
    get filterError() {
        return $('#filter-error');
    }
    get catalogCount() {
        return $('[data-testid="result-count"]');
    }
    get pageSizeSelect() {
        return $('#page-size');
    }
    get previousPageButton() {
        return $('#previous-page');
    }
    get nextPageButton() {
        return $('#next-page');
    }
    get pageInfo() {
        return $('[data-testid="page-info"]');
    }
    get emptyCatalog() {
        return $('[data-testid="empty-catalog"]');
    }
    get cards() {
        return $$('[data-testid="product-card"]');
    }

    // Окно товара
    get detailsDialog() {
        return $('#details');
    }
    get detailsImage() {
        return $('#details-image');
    }
    get detailsName() {
        return $('#details-name');
    }
    get detailsDescription() {
        return $('#details-description');
    }
    get detailsPrice() {
        return $('#details-price');
    }
    get closeDetailsButton() {
        return $('#close-details');
    }

    // Корзина и оформление
    get cartTotal() {
        return $('[data-testid="cart-total"]');
    }
    get emptyCart() {
        return $('[data-testid="empty-cart"]');
    }
    get couponInput() {
        return $('#coupon');
    }
    get applyCouponButton() {
        return $('#apply-coupon');
    }
    get discountTotal() {
        return $('[data-testid="discount-total"]');
    }
    get addressInput() {
        return $('#address');
    }
    get addressError() {
        return $('#address-error');
    }
    get checkoutButton() {
        return $('#checkout');
    }

    // Заказы и подтверждение отмены
    get orderFilterSelect() {
        return $('#order-filter');
    }
    get refreshOrdersButton() {
        return $('#refresh-orders');
    }
    get emptyOrders() {
        return $('[data-testid="empty-orders"]');
    }
    get emptyFilteredOrders() {
        return $('[data-testid="empty-filtered-orders"]');
    }
    get orderCard() {
        return $('[data-testid="order-card"]');
    }
    get orderStatus() {
        return $('[data-testid="order-status"]');
    }
    get orderTotal() {
        return $('[data-testid="order-total"]');
    }
    get cancelDialog() {
        return $('#cancel-dialog');
    }
    get keepOrderButton() {
        return $('#keep-order');
    }
    get confirmCancelButton() {
        return $('#confirm-cancel');
    }

    // Профиль
    get profileEmail() {
        return $('[data-testid="profile-email"]');
    }
    get profileNameInput() {
        return $('#profile-name');
    }
    get profileError() {
        return $('#profile-error');
    }
    get saveProfileButton() {
        return $('#save-profile');
    }

    // Элементы конкретного товара, строки корзины и заказа
    product(id) {
        return $(`[data-testid="product-card"][data-id="${id}"]`);
    }
    cartRow(id) {
        return $(`[data-testid="cart-row"][data-id="${id}"]`);
    }
    orderById(id) {
        return $(`[data-testid="order-card"][data-id="${id}"]`);
    }
    productName(id) {
        return this.product(id).$('h2');
    }
    productImage(id) {
        return this.product(id).$('img');
    }
    productStock(id) {
        return this.product(id).$('[data-testid="product-stock"]');
    }
    productDetailsButton(id) {
        return this.product(id).$('button=Подробнее');
    }
    addToCartButton(id) {
        return this.product(id).$('button=В корзину');
    }
    addFavoriteButton(id) {
        return this.product(id).$('button=В избранное');
    }
    removeFavoriteButton(id) {
        return this.product(id).$('button=Убрать из избранного');
    }
    quantityInput(id) {
        return this.cartRow(id).$('input[type="number"]');
    }
    removeFromCartButton(id) {
        return this.cartRow(id).$('button=Удалить');
    }
    orderStatusFor(id) {
        return this.orderById(id).$('[data-testid="order-status"]');
    }
    orderTotalFor(id) {
        return this.orderById(id).$('[data-testid="order-total"]');
    }
    cancelOrderButton(orderId) {
        return (orderId === undefined ? this.orderCard : this.orderById(orderId)).$(
            'button=Отменить заказ',
        );
    }
    payOrderButton(orderId) {
        return (orderId === undefined ? this.orderCard : this.orderById(orderId)).$(
            'button=Оплатить',
        );
    }

    // Действия: один метод — одно логическое действие
    async enterEmail(email) {
        await this.emailInput.setValue(email);
    }
    async enterPassword(password) {
        await this.passwordInput.setValue(password);
    }
    async enterSearch(name) {
        await this.searchInput.setValue(name);
    }
    async enterMinPrice(price) {
        await this.minPriceInput.setValue(price);
    }
    async enterMaxPrice(price) {
        await this.maxPriceInput.setValue(price);
    }
    async enterCoupon(code) {
        await this.couponInput.setValue(code);
    }
    async enterAddress(address) {
        await this.addressInput.setValue(address);
    }
    async enterProfileName(name) {
        await this.profileNameInput.setValue(name);
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
    async addToCart(id) {
        await this.addToCartButton(id).click();
    }
    async removeFromCart(id) {
        await this.removeFromCartButton(id).click();
    }
    async openProductDetails(id) {
        await this.productDetailsButton(id).click();
    }
    async addToFavorites(id) {
        await this.addFavoriteButton(id).click();
    }
    async removeFromFavorites(id) {
        await this.removeFavoriteButton(id).click();
    }
    async requestCancellation(orderId) {
        await this.cancelOrderButton(orderId).click();
    }
    async payOrder(orderId) {
        await this.payOrderButton(orderId).click();
    }
    async selectCategory(value) {
        await this.categorySelect.selectByAttribute('value', String(value));
    }
    async selectPageSize(value) {
        await this.pageSizeSelect.selectByAttribute('value', String(value));
    }
    async filterOrdersByStatus(value) {
        await this.orderFilterSelect.selectByAttribute('value', String(value));
    }
    async sortProductsByPriceAscending() {
        await this.sortSelect.selectByAttribute('value', 'price_asc');
    }
    async sortProductsByPriceDescending() {
        await this.sortSelect.selectByAttribute('value', 'price_desc');
    }
    async setOnlyInStock(enabled) {
        if ((await this.inStockCheckbox.isSelected()) !== enabled)
            await this.inStockCheckbox.click();
    }
    async setOnlyFavorites(enabled) {
        if ((await this.favoritesOnlyCheckbox.isSelected()) !== enabled)
            await this.favoritesOnlyCheckbox.click();
    }
    async setPasswordVisible(enabled) {
        if ((await this.showPasswordCheckbox.isSelected()) !== enabled)
            await this.showPasswordCheckbox.click();
    }

    async open() {
        await browser.url('/');
        await this.readyBody.waitForExist();
    }
    async refresh() {
        await browser.refresh();
        await this.readyBody.waitForExist();
    }
    async logout() {
        await this.logoutButton.click();
        await this.emailInput.waitForDisplayed();
    }
    async closeProductDetailsWithEscape() {
        await browser.keys('Escape');
    }
    async changeQuantity(id, quantity) {
        await this.quantityInput(id).click();
        await browser.keys([Key.Ctrl, 'a']);
        await browser.keys(String(quantity));
        await browser.keys('Tab');
    }

    // Чтение и ожидания состояния — без бизнес-проверок и фиксированных пауз.
    async productCount() {
        const cards = await this.cards.getElements();
        return cards.length;
    }
    async productIds() {
        const cards = await this.cards.getElements();
        return cards.map(async (card) => Number(await card.getAttribute('data-id')));
    }
    async productPrices() {
        const cards = await this.cards.getElements();
        return cards.map(async (card) => Number(await card.getAttribute('data-price')));
    }
    async waitForOrderStatus(status) {
        // Оплата асинхронная: перезапрашиваем список, пока worker не обработает событие.
        await browser.waitUntil(
            async () => {
                await this.refreshOrders();
                const current = await this.orderStatus;
                return (await current.isExisting()) && (await current.getText()) === status;
            },
            { timeout: 20000, interval: 500, timeoutMsg: `Заказ не получил статус ${status}` },
        );
    }
    async waitForProductIds(ids) {
        await browser.waitUntil(
            async () => {
                // Не читаем исчезающие индексы во время перерисовки каталога.
                if ((await this.productCount()) !== ids.length) return false;
                return JSON.stringify(await this.productIds()) === JSON.stringify(ids);
            },
            { timeoutMsg: 'Каталог не показал ожидаемый набор товаров' },
        );
    }
}

export default new ShopPage();
