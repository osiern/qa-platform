import { test, expect } from '../fixture.js';
import addProductToCart from '../shared/addProductToCart.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import placeOrder from '../shared/placeOrder.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#10
// prio: Critical
// casegroup: Заказы
// team: Academy
// env: local

test('Заказы: отмена требует подтверждения и возвращает остаток', async ({ shop, world }) => {
    const DATA = { address: 'Самара, Учебная улица, 10' };

    await openShop(shop);
    await login(shop, world);
    await searchOwnProducts(shop, world);
    await addProductToCart(shop, world);
    await placeOrder(shop, DATA.address);

    await test.step('it: Открыть каталог', async () => {
        await shop.openCatalog();
    });

    await test.step('it: Нажать «Найти», чтобы перечитать остаток', async () => {
        await shop.submitSearch();
    });

    // Без этой проверки финальная «остаток вернулся» прошла бы и на старых данных.
    await test.step('check: Остаток уменьшился на купленную единицу', async () => {
        await expect(shop.productStock(world.product.id)).toHaveText(
            `В наличии: ${world.product.stock - 1}`,
        );
    });

    await test.step('it: Открыть заказы', async () => {
        await shop.openOrders();
    });

    await test.step('it: Нажать «Отменить заказ»', async () => {
        await shop.requestCancellation();
    });

    await test.step('check: Открыто окно подтверждения', async () => {
        await expect(shop.cancelDialog).toBeVisible();
    });

    await test.step('it: Нажать «Оставить заказ»', async () => {
        await shop.keepOrder();
    });

    await test.step('check: Заказ сохранил статус new', async () => {
        await expect(shop.orderStatus).toHaveText('new');
    });

    await test.step('it: Снова нажать «Отменить заказ»', async () => {
        await shop.requestCancellation();
    });

    await test.step('it: Нажать «Да, отменить»', async () => {
        await shop.confirmCancellation();
    });

    await test.step('check: Заказ получил статус cancelled', async () => {
        await expect(shop.orderStatus).toHaveText('cancelled');
    });

    await test.step('check: Окно подтверждения закрылось', async () => {
        await expect(shop.cancelDialog).toBeHidden();
    });

    await test.step('it: Открыть каталог', async () => {
        await shop.openCatalog();
    });

    await test.step('it: Нажать «Найти», чтобы перечитать остаток', async () => {
        await shop.submitSearch();
    });

    await test.step('check: Остаток вернулся на склад', async () => {
        await expect(shop.productStock(world.product.id)).toHaveText(
            `В наличии: ${world.product.stock}`,
        );
    });
});
