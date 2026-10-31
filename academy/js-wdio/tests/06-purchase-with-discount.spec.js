import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import addProductToCart from '../shared/addProductToCart.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import placeOrder from '../shared/placeOrder.js';
import prepareWorld from '../shared/prepareWorld.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#06
// prio: Blocker
// casegroup: Заказы
// team: Academy
// env: local

describe('Заказы: покупка со скидкой 10% по промокоду', () => {
    const DATA = {
        coupon: 'SAVE10',
        address: 'Самара, Учебная улица, 10',
    };

    // Деньги в копейках и целых числах: округление вниз, как на сервере.
    const discounted = (price) => String(Math.floor((price * 90) / 100));

    const world = prepareWorld();

    openShop();
    login(world);
    searchOwnProducts(world);
    addProductToCart(world);

    it(`Ввести промокод «${DATA.coupon}»`, async () => {
        await Shop.enterCoupon(DATA.coupon);
    });

    it('Нажать «Применить промокод»', async () => {
        await Shop.applyCoupon();
    });

    check('Сумма к оплате уменьшилась на 10%', async () => {
        await expect(Shop.discountTotal).toHaveAttribute(
            'data-cents',
            discounted(world.product.price),
        );
    });

    placeOrder(DATA.address);

    check('Сумма заказа совпадает с суммой со скидкой', async () => {
        await expect(Shop.orderTotal).toHaveAttribute(
            'data-cents',
            discounted(world.product.price),
        );
    });

    it('Открыть корзину', async () => {
        await Shop.openCart();
    });

    check('После покупки корзина пуста', async () => {
        await expect(Shop.emptyCart).toBeDisplayed();
    });
});
