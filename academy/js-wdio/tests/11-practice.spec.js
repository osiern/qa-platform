import { expect } from '@wdio/globals';
import Shop from '../pages/ShopPage.js';
import openShop from '../shared/openShop.js';
import prepareWorld from '../shared/prepareWorld.js';

// project: QA Market
// description: academy/docs/LESSON-01.md
// prio: Blocker
// casegroup: Заказы
// team: Academy
// env: local

// Упражнение. Удали .skip у describe и заполни каждый TODO.
// Один it — одно действие. Один check — один expect.
// Вход и корзину пиши шагами вручную, без shared/login.js — это и есть практика.
// Разборы готовых сценариев: academy/docs/INTERVIEW-E2E.md
describe.skip('Практика: покупка без промокода', () => {
    const DATA = { address: 'Самара, Учебная улица, 10' };

    const world = prepareWorld();

    openShop();

    it('Ввести email', async () => {
        // TODO: await Shop.enterEmail(...) — email лежит в world.user.
        throw new Error('Выполни этот шаг упражнения');
    });

    it('Ввести пароль', async () => {
        // TODO: введи пароль из world.user.
        throw new Error('Выполни этот шаг упражнения');
    });

    it('Нажать «Войти»', async () => {
        // TODO: отправь форму входа.
        throw new Error('Выполни этот шаг упражнения');
    });

    it('Ввести название своего товара', async () => {
        // TODO: название лежит в world.product.
        throw new Error('Выполни этот шаг упражнения');
    });

    it('Нажать «Найти»', async () => {
        // TODO: запусти поиск.
        throw new Error('Выполни этот шаг упражнения');
    });

    auto('Дождаться результата поиска', async () => {
        // TODO: await Shop.waitForProductIds([...]) — без пауз.
        throw new Error('Выполни этот шаг упражнения');
    });

    it('Нажать «В корзину» у своего товара', async () => {
        // TODO: добавь товар по world.product.id.
        throw new Error('Выполни этот шаг упражнения');
    });

    check('Магазин подтвердил добавление', async () => {
        // TODO: один expect для Shop.message.
        throw new Error('Выполни этот шаг упражнения');
    });

    it('Открыть корзину', async () => {
        // TODO: перейди в корзину.
        throw new Error('Выполни этот шаг упражнения');
    });

    check('Сумма корзины равна цене товара', async () => {
        // TODO: один expect для атрибута data-cents у Shop.cartTotal.
        throw new Error('Выполни этот шаг упражнения');
    });

    it('Ввести адрес доставки', async () => {
        // TODO: адрес лежит в DATA.
        throw new Error('Выполни этот шаг упражнения');
    });

    it('Нажать «Оформить заказ»', async () => {
        // TODO: оформи заказ.
        throw new Error('Выполни этот шаг упражнения');
    });

    check('Создан заказ со статусом new', async () => {
        // TODO: один expect для Shop.orderStatus.
        throw new Error('Выполни этот шаг упражнения');
    });

    check('Сумма заказа равна цене товара', async () => {
        // TODO: один expect для атрибута data-cents у Shop.orderTotal.
        throw new Error('Выполни этот шаг упражнения');
    });
});
