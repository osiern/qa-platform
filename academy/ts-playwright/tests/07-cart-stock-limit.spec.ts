import { test, expect } from '../fixture.js';
import addProductToCart from '../shared/addProductToCart.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#07
// prio: Critical
// casegroup: Корзина
// team: Academy
// env: local

// Остаток товара — 10 шт. Сервер отвечает 409 на количество 11.
test('Корзина: количество больше остатка отклоняется, корзина сохраняется', async ({
    shop,
    world,
}) => {
    const DATA = { quantity: 3 };

    await openShop(shop);
    await login(shop, world);
    await searchOwnProducts(shop, world);
    await addProductToCart(shop, world);

    await test.step(`it: Изменить количество на ${DATA.quantity}`, async () => {
        await shop.changeQuantity(world.product.id, DATA.quantity);
    });

    await test.step('check: Корзина подтвердила изменение', async () => {
        await expect(shop.message).toHaveText('Количество обновлено');
    });

    await test.step(`check: Сумма равна цене ${DATA.quantity} шт.`, async () => {
        await expect(shop.cartTotal).toHaveAttribute(
            'data-cents',
            String(world.product.price * DATA.quantity),
        );
    });

    await test.step('it: Изменить количество на число больше остатка', async () => {
        await shop.changeQuantity(world.product.id, world.product.stock + 1);
    });

    await test.step('check: Показана ошибка «Недостаточно товара»', async () => {
        await expect(shop.message).toHaveText('Недостаточно товара');
    });

    await test.step(`check: В поле вернулось сохранённое количество ${DATA.quantity}`, async () => {
        await expect(shop.quantityInput(world.product.id)).toHaveValue(String(DATA.quantity));
    });

    await test.step('it: Обновить страницу', async () => {
        await shop.refresh();
    });

    await test.step('it: Открыть корзину', async () => {
        await shop.openCart();
    });

    await test.step(`check: После обновления в корзине ${DATA.quantity} шт.`, async () => {
        await expect(shop.quantityInput(world.product.id)).toHaveValue(String(DATA.quantity));
    });
});
