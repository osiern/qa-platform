import { test, expect } from '../fixture.js';
import openShop from '../shared/openShop.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#05
// prio: Normal
// casegroup: Каталог
// team: Academy
// env: local

// 4 товара при 3 на странице: полная первая страница и неполная последняя.
test.use({ productCount: 4 });

test('Каталог: переход между страницами без дублей и пропусков', async ({ shop, world }) => {
    const DATA = { pageSize: 3 };
    const firstPage = world.products.slice(0, DATA.pageSize).map((product) => product.id);

    await openShop(shop);
    await searchOwnProducts(shop, world, { all: true });

    await test.step(`it: Выбрать «Товаров на странице: ${DATA.pageSize}»`, async () => {
        await shop.selectPageSize(DATA.pageSize);
    });

    await test.step('auto: Дождаться первой страницы', async () => {
        await shop.waitForProductIds(firstPage);
    });

    await test.step('check: На первой странице кнопка «Назад» недоступна', async () => {
        await expect(shop.previousPageButton).toBeDisabled();
    });

    await test.step('it: Нажать «Далее»', async () => {
        await shop.nextPage();
    });

    await test.step('auto: Дождаться второй страницы', async () => {
        await shop.waitForProductIds([world.products[3].id]);
    });

    await test.step('check: На второй странице только четвёртый товар', async () => {
        await expect.poll(() => shop.productIds()).toEqual([world.products[3].id]);
    });

    await test.step('check: На последней странице кнопка «Далее» недоступна', async () => {
        await expect(shop.nextPageButton).toBeDisabled();
    });

    await test.step('it: Нажать «Назад»', async () => {
        await shop.previousPage();
    });

    await test.step('auto: Дождаться первой страницы повторно', async () => {
        await shop.waitForProductIds(firstPage);
    });

    await test.step('check: Отображается «Страница 1 из 2»', async () => {
        await expect(shop.pageInfo).toHaveText('Страница 1 из 2');
    });
});
