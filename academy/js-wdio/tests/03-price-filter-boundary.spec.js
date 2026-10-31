import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import openShop from '../shared/openShop.js';
import prepareWorld from '../shared/prepareWorld.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#03
// prio: Normal
// casegroup: Каталог
// team: Academy
// env: local

describe('Каталог: обе границы диапазона цен включены в фильтр', () => {
    // Цены товаров: 1234, 1334 и 1434 ₽. Диапазон — от первой до второй цены.
    const world = prepareWorld({ productCount: 3 });

    openShop();
    searchOwnProducts(world, { all: true });

    it('Ввести «Цена от» равной цене первого товара', async () => {
        await Shop.enterMinPrice(world.products[0].price / 100);
    });

    it('Ввести «Цена до» равной цене второго товара', async () => {
        await Shop.enterMaxPrice(world.products[1].price / 100);
    });

    it('Нажать «Найти»', async () => {
        await Shop.submitSearch();
    });

    auto('Дождаться отфильтрованной выдачи', async () => {
        await Shop.waitForProductIds([world.products[0].id, world.products[1].id]);
    });

    check('В выдаче оба товара на границах и нет товара за верхней границей', async () => {
        await expect(await Shop.productIds()).toEqual([world.products[0].id, world.products[1].id]);
    });

    check('Счётчик показывает два товара', async () => {
        await expect(Shop.catalogCount).toHaveAttribute('data-count', '2');
    });
});
