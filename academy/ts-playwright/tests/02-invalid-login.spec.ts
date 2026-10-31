import { test, expect } from '../fixture.js';
import openShop from '../shared/openShop.js';

// project: QA Market
// description: academy/docs/CASES.md#02
// prio: Critical
// casegroup: Авторизация
// team: Academy
// env: local

test('Авторизация: неверный пароль не открывает аккаунт', async ({ shop, world }) => {
    const DATA = {
        password: 'Wrong-password-123',
        error: 'Неверный email или пароль',
    };

    await openShop(shop);

    await test.step('it: Ввести email существующего пользователя', async () => {
        await shop.enterEmail(world.user.email);
    });

    await test.step('it: Ввести неверный пароль', async () => {
        await shop.enterPassword(DATA.password);
    });

    await test.step('it: Нажать «Войти»', async () => {
        await shop.submitLogin();
    });

    await test.step(`check: Показана общая ошибка «${DATA.error}»`, async () => {
        await expect(shop.message).toHaveText(DATA.error);
    });

    await test.step('check: Форма входа осталась открытой', async () => {
        await expect(shop.emailInput).toBeVisible();
    });

    await test.step('check: Пользователь не авторизован', async () => {
        await expect(shop.identity).toHaveCount(0);
    });
});
