import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';
import prepareWorld from '../shared/prepareWorld.js';

// project: QA Market
// description: academy/docs/CASES.md#01
// prio: Critical
// casegroup: Авторизация
// team: Academy
// env: local

describe('Авторизация: вход, сохранение сессии после обновления и выход', () => {
    const world = prepareWorld();

    openShop();
    login(world);

    it('Открыть профиль', async () => {
        await Shop.openProfile();
    });

    check('В профиле отображается email пользователя', async () => {
        await expect(Shop.profileEmail).toHaveText(world.user.email);
    });

    it('Обновить страницу', async () => {
        await Shop.refresh();
    });

    check('После обновления пользователь остаётся авторизован', async () => {
        await expect(Shop.identity).toHaveText(world.user.email);
    });

    it('Нажать «Выйти»', async () => {
        await Shop.logout();
    });

    check('Снова показана форма входа', async () => {
        await expect(Shop.emailInput).toBeDisplayed();
    });

    check('Email исчез из шапки', async () => {
        await expect(Shop.identity).not.toExist();
    });
});
