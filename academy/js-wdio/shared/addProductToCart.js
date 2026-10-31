import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';

/**
 * Регистрирует добавление первого товара сценария в корзину и переход в неё.
 *
 * @param {import('../../support/world.mjs').World} world
 */
export default function addProductToCart(world) {
    it('Нажать «В корзину» у своего товара', async () => {
        await Shop.addToCart(world.product.id);
    });

    check('Магазин подтвердил добавление', async () => {
        await expect(Shop.message).toHaveText('Товар добавлен');
    });

    it('Открыть корзину', async () => {
        await Shop.openCart();
    });

    check('Товар отображается в корзине', async () => {
        await expect(Shop.cartRow(world.product.id)).toBeDisplayed();
    });
}
