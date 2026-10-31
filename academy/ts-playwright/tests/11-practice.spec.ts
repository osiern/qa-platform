import { test, expect } from '../fixture.js';

// project: QA Market
// description: academy/docs/LESSON-01.md
// prio: Blocker
// casegroup: Заказы
// team: Academy
// env: local

// Упражнение. Удали .skip, замени каждый throw на одно действие или одну проверку.
// Вход и корзину пиши шагами вручную, без shared/login.ts — это и есть практика.
test.skip('Практика: покупка без промокода', async ({ shop, world }) => {
    const DATA = { address: 'Самара, Учебная улица, 10' };
    await test.step('pre: Открыть магазин', async () => {
        await shop.open();
    });
    await test.step('it: Ввести email', async () => {
        // TODO: Ввести email
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('it: Ввести пароль', async () => {
        // TODO: Ввести пароль
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('it: Нажать «Войти»', async () => {
        // TODO: Нажать «Войти»
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('it: Ввести название товара в поиск', async () => {
        // TODO: Ввести название товара в поиск
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('it: Нажать «Найти»', async () => {
        // TODO: Нажать «Найти»
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('it: Добавить товар в корзину', async () => {
        // TODO: Добавить товар в корзину
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('check: Магазин подтвердил добавление товара', async () => {
        // TODO: Магазин подтвердил добавление товара
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('it: Открыть корзину', async () => {
        // TODO: Открыть корзину
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('check: Сумма корзины равна цене товара', async () => {
        // TODO: Сумма корзины равна цене товара
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('it: Ввести адрес доставки', async () => {
        // TODO: Ввести адрес доставки
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('it: Оформить заказ', async () => {
        // TODO: Оформить заказ
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('check: Заказ имеет статус new', async () => {
        // TODO: Заказ имеет статус new
        throw new Error('Выполни шаг упражнения');
    });
    await test.step('check: Сумма заказа равна цене товара', async () => {
        // TODO: Сумма заказа равна цене товара
        throw new Error('Выполни шаг упражнения');
    });
});
