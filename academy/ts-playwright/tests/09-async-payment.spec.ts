import { test, expect } from '../fixture.js';
import addProductToCart from '../shared/addProductToCart.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import placeOrder from '../shared/placeOrder.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#09
// prio: Critical
// casegroup: Оплата
// team: Academy
// env: local

test('Оплата: асинхронная оплата переводит заказ в paid', async ({ shop, world }) => {
    const DATA = { address: 'Самара, Учебная улица, 10' };

    await openShop(shop);
    await login(shop, world);
    await searchOwnProducts(shop, world);
    await addProductToCart(shop, world);
    await placeOrder(shop, DATA.address);

    await test.step('it: Нажать «Оплатить»', async () => {
        await shop.payOrder();
    });

    await test.step('check: Магазин принял оплату в обработку', async () => {
        await expect(shop.message).toHaveText('Оплата передана в обработку');
    });

    // Промежуточный payment_pending не проверяем: worker может успеть раньше.
    // Ждём конечное состояние, а не фиксированную паузу.
    await test.step('auto: Обновлять список заказов, пока worker не обработает оплату', async () => {
        await shop.waitForOrderStatus('paid');
    });

    await test.step('check: Заказ получил статус paid', async () => {
        await expect(shop.orderStatus).toHaveText('paid');
    });

    await test.step('check: Оплаченный заказ нельзя отменить', async () => {
        await expect(shop.cancelOrderButton()).toHaveCount(0);
    });
});
