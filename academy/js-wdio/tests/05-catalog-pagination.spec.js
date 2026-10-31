import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import openShop from '../shared/openShop.js';
import prepareWorld from '../shared/prepareWorld.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#05
// prio: Normal
// casegroup: Каталог
// team: Academy
// env: local

describe('Каталог: переход между страницами без дублей и пропусков', () => {
    const DATA = { pageSize: 3 };

    // 4 товара при 3 на странице: полная первая страница и неполная последняя.
    const world = prepareWorld({ productCount: 4 });

    openShop();
    searchOwnProducts(world, { all: true });

    it(`Выбрать «Товаров на странице: ${DATA.pageSize}»`, async () => {
        await Shop.selectPageSize(DATA.pageSize);
    });

    auto('Дождаться первой страницы', async () => {
        await Shop.waitForProductIds(
            world.products.slice(0, DATA.pageSize).map((product) => product.id),
        );
    });

    check('На первой странице кнопка «Назад» недоступна', async () => {
        await expect(Shop.previousPageButton).not.toBeEnabled();
    });

    it('Нажать «Далее»', async () => {
        await Shop.nextPage();
    });

    auto('Дождаться второй страницы', async () => {
        await Shop.waitForProductIds([world.products[3].id]);
    });

    check('На второй странице только четвёртый товар', async () => {
        await expect(await Shop.productIds()).toEqual([world.products[3].id]);
    });

    check('На последней странице кнопка «Далее» недоступна', async () => {
        await expect(Shop.nextPageButton).not.toBeEnabled();
    });

    it('Нажать «Назад»', async () => {
        await Shop.previousPage();
    });

    auto('Дождаться первой страницы повторно', async () => {
        await Shop.waitForProductIds(
            world.products.slice(0, DATA.pageSize).map((product) => product.id),
        );
    });

    check('Отображается «Страница 1 из 2»', async () => {
        await expect(Shop.pageInfo).toHaveText('Страница 1 из 2');
    });
});
