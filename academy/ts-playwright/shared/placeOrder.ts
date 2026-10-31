import { expect, test } from '../fixture.js';
import type { ShopPage } from '../pages/ShopPage.js';

/** Оформление заказа из открытой корзины. Адрес — от 5 до 300 символов. */
export default async function placeOrder(shop: ShopPage, address: string) {
    await test.step('it: Ввести адрес доставки', async () => {
        await shop.enterAddress(address);
    });

    await test.step('it: Нажать «Оформить заказ»', async () => {
        await shop.submitOrder();
    });

    await test.step('check: Создан заказ со статусом new', async () => {
        await expect(shop.orderStatus).toHaveText('new');
    });
}
