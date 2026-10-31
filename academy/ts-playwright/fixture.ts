import { test as base, expect } from '@playwright/test';
import { createWorld, type World } from '../support/world.mjs';
import { ShopPage } from './pages/ShopPage.js';

export const test = base.extend<{ world: World; shop: ShopPage; productCount: number }>({
    productCount: [1, { option: true }],
    world: async ({ productCount }, use) => {
        const world = await base.step('pre: создать пользователя и товары через API', () =>
            createWorld({ productCount }),
        );
        try {
            await use(world);
        } finally {
            await world.cleanup();
        }
    },
    shop: async ({ page, world }, use) => {
        await use(new ShopPage(page));
    },
});
export { expect };
