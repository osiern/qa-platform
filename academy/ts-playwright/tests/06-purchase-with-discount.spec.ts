import { test, expect } from '../fixture.js';
import addProductToCart from '../shared/addProductToCart.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import placeOrder from '../shared/placeOrder.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#06
// prio: Blocker
// casegroup: Заказы
// team: Academy
// env: local

// Деньги в копейках и целых числах: округление вниз, как на сервере.
const discounted = (price: number) => String(Math.floor((price * 90) / 100));

test('Заказы: покупка со скидкой 10% по промокоду', async ({ shop, world }) => {
    const DATA = {
        coupon: 'SAVE10',
        address: 'Самара, Учебная улица, 10',
    };

    await openShop(shop);
    await login(shop, world);
    await searchOwnProducts(shop, world);
    await addProductToCart(shop, world);

    await test.step(`it: Ввести промокод «${DATA.coupon}»`, async () => {
        await shop.enterCoupon(DATA.coupon);
    });

    await test.step('it: Нажать «Применить промокод»', async () => {
        await shop.applyCoupon();
    });

    await test.step('check: Сумма к оплате уменьшилась на 10%', async () => {
        await expect(shop.discountTotal).toHaveAttribute(
            'data-cents',
            discounted(world.product.price),
        );
    });

    await placeOrder(shop, DATA.address);

    await test.step('check: Сумма заказа совпадает с суммой со скидкой', async () => {
        await expect(shop.orderTotal).toHaveAttribute(
            'data-cents',
            discounted(world.product.price),
        );
    });

    await test.step('it: Открыть корзину', async () => {
        await shop.openCart();
    });

    await test.step('check: После покупки корзина пуста', async () => {
        await expect(shop.emptyCart).toBeVisible();
    });
});
