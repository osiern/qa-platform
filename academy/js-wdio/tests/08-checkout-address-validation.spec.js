import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import addProductToCart from '../shared/addProductToCart.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import prepareWorld from '../shared/prepareWorld.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#08
// prio: Critical
// casegroup: Заказы
// team: Academy
// env: local

describe('Заказы: адрес короче 5 символов не создаёт заказ', () => {
    // Граница поля — 5–300 символов. 4 — ближайшее недопустимое значение.
    const DATA = {
        address: '1234',
        error: 'Укажите адрес: от 5 до 300 символов',
    };

    const world = prepareWorld();

    openShop();
    login(world);
    searchOwnProducts(world);
    addProductToCart(world);

    it('Ввести адрес из 4 символов', async () => {
        await Shop.enterAddress(DATA.address);
    });

    it('Нажать «Оформить заказ»', async () => {
        await Shop.submitOrder();
    });

    check('Показана ошибка длины адреса', async () => {
        await expect(Shop.addressError).toHaveText(DATA.error);
    });

    check('Поле адреса отмечено aria-invalid', async () => {
        await expect(Shop.addressInput).toHaveAttribute('aria-invalid', 'true');
    });

    check('Товар остался в корзине', async () => {
        await expect(Shop.cartRow(world.product.id)).toBeDisplayed();
    });

    it('Открыть заказы', async () => {
        await Shop.openOrders();
    });

    check('Заказ не создан', async () => {
        await expect(Shop.emptyOrders).toBeDisplayed();
    });
});
