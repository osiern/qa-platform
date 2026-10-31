import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import addProductToCart from '../shared/addProductToCart.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import placeOrder from '../shared/placeOrder.js';
import prepareWorld from '../shared/prepareWorld.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#10
// prio: Critical
// casegroup: Заказы
// team: Academy
// env: local

describe('Заказы: отмена требует подтверждения и возвращает остаток', () => {
    const DATA = { address: 'Самара, Учебная улица, 10' };

    const world = prepareWorld();

    openShop();
    login(world);
    searchOwnProducts(world);
    addProductToCart(world);
    placeOrder(DATA.address);

    it('Открыть каталог', async () => {
        await Shop.openCatalog();
    });

    it('Нажать «Найти», чтобы перечитать остаток', async () => {
        await Shop.submitSearch();
    });

    // Без этой проверки финальная «остаток вернулся» прошла бы и на старых данных.
    check('Остаток уменьшился на купленную единицу', async () => {
        await expect(Shop.productStock(world.product.id)).toHaveText(
            `В наличии: ${world.product.stock - 1}`,
        );
    });

    it('Открыть заказы', async () => {
        await Shop.openOrders();
    });

    it('Нажать «Отменить заказ»', async () => {
        await Shop.requestCancellation();
    });

    check('Открыто окно подтверждения', async () => {
        await expect(Shop.cancelDialog).toBeDisplayed();
    });

    it('Нажать «Оставить заказ»', async () => {
        await Shop.keepOrder();
    });

    check('Заказ сохранил статус new', async () => {
        await expect(Shop.orderStatus).toHaveText('new');
    });

    it('Снова нажать «Отменить заказ»', async () => {
        await Shop.requestCancellation();
    });

    it('Нажать «Да, отменить»', async () => {
        await Shop.confirmCancellation();
    });

    check('Заказ получил статус cancelled', async () => {
        await expect(Shop.orderStatus).toHaveText('cancelled');
    });

    check('Окно подтверждения закрылось', async () => {
        await expect(Shop.cancelDialog).not.toBeDisplayed();
    });

    it('Открыть каталог', async () => {
        await Shop.openCatalog();
    });

    it('Нажать «Найти», чтобы перечитать остаток', async () => {
        await Shop.submitSearch();
    });

    check('Остаток вернулся на склад', async () => {
        await expect(Shop.productStock(world.product.id)).toHaveText(
            `В наличии: ${world.product.stock}`,
        );
    });
});
