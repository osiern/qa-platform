import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import addProductToCart from '../shared/addProductToCart.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import prepareWorld from '../shared/prepareWorld.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#07
// prio: Critical
// casegroup: Корзина
// team: Academy
// env: local

describe('Корзина: количество больше остатка отклоняется, корзина сохраняется', () => {
    const DATA = { quantity: 3 };

    // Остаток товара — 10 шт. Сервер отвечает 409 на количество 11.
    const world = prepareWorld();

    openShop();
    login(world);
    searchOwnProducts(world);
    addProductToCart(world);

    it(`Изменить количество на ${DATA.quantity}`, async () => {
        await Shop.changeQuantity(world.product.id, DATA.quantity);
    });

    check('Корзина подтвердила изменение', async () => {
        await expect(Shop.message).toHaveText('Количество обновлено');
    });

    check(`Сумма равна цене ${DATA.quantity} шт.`, async () => {
        await expect(Shop.cartTotal).toHaveAttribute(
            'data-cents',
            String(world.product.price * DATA.quantity),
        );
    });

    it('Изменить количество на число больше остатка', async () => {
        await Shop.changeQuantity(world.product.id, world.product.stock + 1);
    });

    check('Показана ошибка «Недостаточно товара»', async () => {
        await expect(Shop.message).toHaveText('Недостаточно товара');
    });

    check(`В поле вернулось сохранённое количество ${DATA.quantity}`, async () => {
        await expect(Shop.quantityInput(world.product.id)).toHaveValue(String(DATA.quantity));
    });

    it('Обновить страницу', async () => {
        await Shop.refresh();
    });

    it('Открыть корзину', async () => {
        await Shop.openCart();
    });

    check(`После обновления в корзине ${DATA.quantity} шт.`, async () => {
        await expect(Shop.quantityInput(world.product.id)).toHaveValue(String(DATA.quantity));
    });
});
