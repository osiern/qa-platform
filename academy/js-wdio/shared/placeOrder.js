import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';

/**
 * Регистрирует оформление заказа из открытой корзины.
 *
 * @param {string} address Адрес доставки от 5 до 300 символов
 */
export default function placeOrder(address) {
    it('Ввести адрес доставки', async () => {
        await Shop.enterAddress(address);
    });

    it('Нажать «Оформить заказ»', async () => {
        await Shop.submitOrder();
    });

    check('Создан заказ со статусом new', async () => {
        await expect(Shop.orderStatus).toHaveText('new');
    });
}
