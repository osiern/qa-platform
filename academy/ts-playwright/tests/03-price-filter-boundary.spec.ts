import { test, expect } from '../fixture.js';
import openShop from '../shared/openShop.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#03
// prio: Normal
// casegroup: Каталог
// team: Academy
// env: local

// Цены товаров: 1234, 1334 и 1434 ₽. Диапазон — от первой до второй цены.
test.use({ productCount: 3 });

test('Каталог: обе границы диапазона цен включены в фильтр', async ({ shop, world }) => {
    const inRange = [world.products[0].id, world.products[1].id];

    await openShop(shop);
    await searchOwnProducts(shop, world, { all: true });

    await test.step('it: Ввести «Цена от» равной цене первого товара', async () => {
        await shop.enterMinPrice(world.products[0].price / 100);
    });

    await test.step('it: Ввести «Цена до» равной цене второго товара', async () => {
        await shop.enterMaxPrice(world.products[1].price / 100);
    });

    await test.step('it: Нажать «Найти»', async () => {
        await shop.submitSearch();
    });

    await test.step('auto: Дождаться отфильтрованной выдачи', async () => {
        await shop.waitForProductIds(inRange);
    });

    await test.step('check: В выдаче оба товара на границах и нет товара за верхней границей', async () => {
        await expect.poll(() => shop.productIds()).toEqual(inRange);
    });

    await test.step('check: Счётчик показывает два товара', async () => {
        await expect(shop.catalogCount).toHaveAttribute('data-count', '2');
    });
});
