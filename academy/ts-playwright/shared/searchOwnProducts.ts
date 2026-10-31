import { test } from '../fixture.js';
import type { ShopPage } from '../pages/ShopPage.js';
import type { World } from '../../support/world.mjs';

/**
 * Поиск товаров, созданных для сценария.
 * all=false — только первый товар по точному названию,
 * all=true — все товары по общему префиксу.
 */
export default async function searchOwnProducts(
    shop: ShopPage,
    world: World,
    { all = false }: { all?: boolean } = {},
) {
    const title = all ? 'Ввести общий префикс своих товаров' : 'Ввести название своего товара';
    await test.step(`it: ${title}`, async () => {
        await shop.enterSearch(all ? world.searchPrefix : world.product.name);
    });

    await test.step('it: Нажать «Найти»', async () => {
        await shop.submitSearch();
    });

    await test.step('auto: Дождаться результата поиска', async () => {
        const ids = all ? world.products.map((product) => product.id) : [world.product.id];
        await shop.waitForProductIds(ids);
    });
}
