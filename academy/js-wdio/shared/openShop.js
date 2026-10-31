import Shop from '../pages/ShopPage.js';

/** Регистрирует шаг открытия магазина. */
export default function openShop() {
    pre('Открыть магазин', async () => {
        await Shop.open();
    });
}
