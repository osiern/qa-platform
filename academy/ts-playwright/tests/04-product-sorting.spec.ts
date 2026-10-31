import { test, expect } from '../fixture.js';
import openShop from '../shared/openShop.js';
import searchOwnProducts from '../shared/searchOwnProducts.js';

// project: QA Market
// description: academy/docs/CASES.md#04
// prio: Normal
// casegroup: Каталог
// team: Academy
// env: local

test.use({ productCount: 3 });

test('Каталог: сортировка товаров по возрастанию цены', async ({ shop, world }) => {
    await openShop(shop);
    await searchOwnProducts(shop, world, { all: true });

    // Без обратного порядка проверка «по возрастанию» прошла бы и без сортировки:
    // товары созданы в порядке роста цены.
    await test.step('it: Выбрать сортировку «Сначала дороже»', async () => {
        await shop.sortProductsByPriceDescending();
    });

    await test.step('auto: Дождаться обратного порядка', async () => {
        await shop.waitForProductIds([...world.products].reverse().map((product) => product.id));
    });

    await test.step('it: Выбрать сортировку «Сначала дешевле»', async () => {
        await shop.sortProductsByPriceAscending();
    });

    await test.step('auto: Дождаться завершения сортировки', async () => {
        await shop.waitForProductIds(
            [...world.products].sort((a, b) => a.price - b.price).map((product) => product.id),
        );
    });

    await test.step('check: Цены идут по возрастанию', async () => {
        await expect
            .poll(() => shop.productPrices())
            .toEqual(world.products.map((product) => product.price).sort((a, b) => a - b));
    });
});
