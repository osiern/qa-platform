import { expect, test } from '../fixture.js';
import type { ShopPage } from '../pages/ShopPage.js';
import type { World } from '../../support/world.mjs';

/** Вход через форму и проверка email в шапке. */
export default async function login(shop: ShopPage, world: World) {
    await test.step('it: Ввести email', async () => {
        await shop.enterEmail(world.user.email);
    });

    await test.step('it: Ввести пароль', async () => {
        await shop.enterPassword(world.user.password);
    });

    await test.step('it: Нажать «Войти»', async () => {
        await shop.submitLogin();
    });

    await test.step('check: Email пользователя отображается в шапке', async () => {
        await expect(shop.identity).toHaveText(world.user.email);
    });
}
