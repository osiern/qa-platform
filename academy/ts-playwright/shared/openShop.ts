import { test } from '../fixture.js';
import type { ShopPage } from '../pages/ShopPage.js';

/** Шаг открытия магазина. */
export default async function openShop(shop: ShopPage) {
    await test.step('pre: Открыть магазин', async () => {
        await shop.open();
    });
}
