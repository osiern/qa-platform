import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import addProductToCart from '../shared/addProductToCart.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import placeOrder from '../shared/placeOrder.js';
import prepareWorld from '../shared/prepareWorld.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#09
// prio: Critical
// casegroup: Оплата
// team: Academy
// env: local

describe('Оплата: асинхронная оплата переводит заказ в paid', () => {
    const DATA = { address: 'Самара, Учебная улица, 10' };

    const world = prepareWorld();

    openShop();
    login(world);
    searchOwnProducts(world);
    addProductToCart(world);
    placeOrder(DATA.address);

    it('Нажать «Оплатить»', async () => {
        await Shop.payOrder();
    });

    check('Магазин принял оплату в обработку', async () => {
        await expect(Shop.message).toHaveText('Оплата передана в обработку');
    });

    // Промежуточный payment_pending не проверяем: worker может успеть раньше.
    // Ждём конечное состояние, а не фиксированную паузу.
    auto('Обновлять список заказов, пока worker не обработает оплату', async () => {
        await Shop.waitForOrderStatus('paid');
    });

    check('Заказ получил статус paid', async () => {
        await expect(Shop.orderStatus).toHaveText('paid');
    });

    check('Оплаченный заказ нельзя отменить', async () => {
        await expect(Shop.cancelOrderButton()).not.toExist();
    });
});
