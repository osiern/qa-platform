import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import openShop from '../shared/openShop.js';
import prepareWorld from '../shared/prepareWorld.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#04
// prio: Normal
// casegroup: Каталог
// team: Academy
// env: local

describe('Каталог: сортировка товаров по возрастанию цены', () => {
    const world = prepareWorld({ productCount: 3 });

    openShop();
    searchOwnProducts(world, { all: true });

    // Без обратного порядка проверка «по возрастанию» прошла бы и без сортировки:
    // товары созданы в порядке роста цены.
    it('Выбрать сортировку «Сначала дороже»', async () => {
        await Shop.sortProductsByPriceDescending();
    });

    auto('Дождаться обратного порядка', async () => {
        await Shop.waitForProductIds([...world.products].reverse().map((product) => product.id));
    });

    it('Выбрать сортировку «Сначала дешевле»', async () => {
        await Shop.sortProductsByPriceAscending();
    });

    auto('Дождаться завершения сортировки', async () => {
        await Shop.waitForProductIds(
            [...world.products].sort((a, b) => a.price - b.price).map((product) => product.id),
        );
    });

    check('Цены идут по возрастанию', async () => {
        await expect(await Shop.productPrices()).toEqual(
            world.products.map((product) => product.price).sort((a, b) => a - b),
        );
    });
});
