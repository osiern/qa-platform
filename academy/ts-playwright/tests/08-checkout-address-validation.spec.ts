import { test, expect } from '../fixture.js';
import addProductToCart from '../shared/addProductToCart.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#08
// prio: Critical
// casegroup: Заказы
// team: Academy
// env: local

test('Заказы: адрес короче 5 символов не создаёт заказ', async ({ shop, world }) => {
    // Граница поля — 5–300 символов. 4 — ближайшее недопустимое значение.
    const DATA = {
        address: '1234',
        error: 'Укажите адрес: от 5 до 300 символов',
    };

    await openShop(shop);
    await login(shop, world);
    await searchOwnProducts(shop, world);
    await addProductToCart(shop, world);

    await test.step('it: Ввести адрес из 4 символов', async () => {
        await shop.enterAddress(DATA.address);
    });

    await test.step('it: Нажать «Оформить заказ»', async () => {
        await shop.submitOrder();
    });

    await test.step('check: Показана ошибка длины адреса', async () => {
        await expect(shop.addressError).toHaveText(DATA.error);
    });

    await test.step('check: Поле адреса отмечено aria-invalid', async () => {
        await expect(shop.addressInput).toHaveAttribute('aria-invalid', 'true');
    });

    await test.step('check: Товар остался в корзине', async () => {
        await expect(shop.cartRow(world.product.id)).toBeVisible();
    });

    await test.step('it: Открыть заказы', async () => {
        await shop.openOrders();
    });

    await test.step('check: Заказ не создан', async () => {
        await expect(shop.emptyOrders).toBeVisible();
    });
});
