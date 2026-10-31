import { test, expect } from '../fixture.js';
import login from '../shared/login.js';
import openShop from '../shared/openShop.js';

// project: QA Market
// description: academy/docs/CASES.md#01
// prio: Critical
// casegroup: Авторизация
// team: Academy
// env: local

test('Авторизация: вход, сохранение сессии после обновления и выход', async ({ shop, world }) => {
    await openShop(shop);
    await login(shop, world);

    await test.step('it: Открыть профиль', async () => {
        await shop.openProfile();
    });

    await test.step('check: В профиле отображается email пользователя', async () => {
        await expect(shop.profileEmail).toHaveText(world.user.email);
    });

    await test.step('it: Обновить страницу', async () => {
        await shop.refresh();
    });

    await test.step('check: После обновления пользователь остаётся авторизован', async () => {
        await expect(shop.identity).toHaveText(world.user.email);
    });

    await test.step('it: Нажать «Выйти»', async () => {
        await shop.logout();
    });

    await test.step('check: Снова показана форма входа', async () => {
        await expect(shop.emailInput).toBeVisible();
    });

    await test.step('check: Email исчез из шапки', async () => {
        await expect(shop.identity).toHaveCount(0);
    });
});
