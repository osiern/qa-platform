import { expect, test } from '../fixture.js';
import type { ShopPage } from '../pages/ShopPage.js';
import type { World } from '../../support/world.mjs';

/** Добавление первого товара сценария в корзину и переход в неё. */
export default async function addProductToCart(shop: ShopPage, world: World) {
    await test.step('it: Нажать «В корзину» у своего товара', async () => {
        await shop.addToCart(world.product.id);
    });

    await test.step('check: Магазин подтвердил добавление', async () => {
        await expect(shop.message).toHaveText('Товар добавлен');
    });

    await test.step('it: Открыть корзину', async () => {
        await shop.openCart();
    });

    await test.step('check: Товар отображается в корзине', async () => {
        await expect(shop.cartRow(world.product.id)).toBeVisible();
    });
}
