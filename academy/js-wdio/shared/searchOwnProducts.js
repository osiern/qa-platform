import Shop from '../pages/ShopPage.js';

/**
 * Регистрирует поиск товаров, созданных для сценария.
 * all=false — только первый товар по точному названию,
 * all=true — все товары по общему префиксу.
 *
 * @param {import('../../support/world.mjs').World} world
 * @param {{all?: boolean}} [options]
 */
export default function searchOwnProducts(world, { all = false } = {}) {
    it(all ? 'Ввести общий префикс своих товаров' : 'Ввести название своего товара', async () => {
        await Shop.enterSearch(all ? world.searchPrefix : world.product.name);
    });

    it('Нажать «Найти»', async () => {
        await Shop.submitSearch();
    });

    auto('Дождаться результата поиска', async () => {
        const ids = all ? world.products.map((product) => product.id) : [world.product.id];
        await Shop.waitForProductIds(ids);
    });
}
