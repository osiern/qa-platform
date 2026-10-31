import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import openShop from '../shared/openShop.js';
import prepareWorld from '../shared/prepareWorld.js';

// project: QA Market
// description: academy/docs/CASES.md#02
// prio: Critical
// casegroup: Авторизация
// team: Academy
// env: local

describe('Авторизация: неверный пароль не открывает аккаунт', () => {
    const DATA = {
        password: 'Wrong-password-123',
        error: 'Неверный email или пароль',
    };

    const world = prepareWorld();

    openShop();

    it('Ввести email существующего пользователя', async () => {
        await Shop.enterEmail(world.user.email);
    });

    it('Ввести неверный пароль', async () => {
        await Shop.enterPassword(DATA.password);
    });

    it('Нажать «Войти»', async () => {
        await Shop.submitLogin();
    });

    check(`Показана общая ошибка «${DATA.error}»`, async () => {
        await expect(Shop.message).toHaveText(DATA.error);
    });

    check('Форма входа осталась открытой', async () => {
        await expect(Shop.emailInput).toBeDisplayed();
    });

    check('Пользователь не авторизован', async () => {
        await expect(Shop.identity).not.toExist();
    });
});
