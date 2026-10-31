import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';

/**
 * Регистрирует вход через форму и проверку email в шапке.
 *
 * @param {{user: {email: string, password: string}}} world
 */
export default function login(world) {
    it('Ввести email', async () => {
        await Shop.enterEmail(world.user.email);
    });

    it('Ввести пароль', async () => {
        await Shop.enterPassword(world.user.password);
    });

    it('Нажать «Войти»', async () => {
        await Shop.submitLogin();
    });

    check('Email пользователя отображается в шапке', async () => {
        await expect(Shop.identity).toHaveText(world.user.email);
    });
}
