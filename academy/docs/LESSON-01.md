# Практика: покупка без промокода

1. Открой `js-wdio/tests/11-practice.spec.js`. Это один сценарий с готовой подготовкой через API.
2. Удали `.skip` у `describe`. Пока TODO не заполнены, шаги намеренно падают.
3. Заполни действия: ввод email, ввод пароля, вход, ввод названия товара, поиск, добавление в корзину, открытие корзины, адрес и оформление заказа. Каждое действие остаётся в своём `it`.
4. В каждом `check` напиши ровно один `expect`: подтверждение добавления, сумма корзины, статус заказа и сумма заказа.
5. Данные пользователя бери из `world.user`, товар — из `world.product`. Его цена хранится в копейках. Адрес уже записан в `DATA`. Объект `world` заполняется в шаге pre, поэтому читай его только внутри шагов.
6. Методы и элементы ищи в `js-wdio/pages/ShopPage.js`. Он подключён как `Shop`. Селекторы в тест не добавляй. Хелперы из `shared/` здесь не используй: вход и корзину пишешь шагами сама/сам.
7. Запусти `npm run practice:js` из `academy`.

Подсказка для действия: `await Shop.enterEmail(world.user.email)`.
Подсказка для проверки: `await expect(Shop.identity).toHaveText(world.user.email)`.
Для цены используй `toHaveAttribute('data-cents', String(...))`.

Сначала попробуй сама/сам. Затем сравни шаги с `06-purchase-with-discount.spec.js`: в упражнении промокод не вводится, поэтому итоговая сумма равна исходной цене товара.

Объясни: зачем await, чем геттер отличается от метода, почему данные создаются через API, почему проверка вынесена в check.

## Повтори на TS и Python

TS: `ts-playwright/tests/11-practice.spec.ts`. Шаги — test.step, методы camelCase с await. Удали .skip у test. Запуск из academy: `npm run practice:ts`.

Python: `python-playwright/tests/test_11_practice.py`. Шаги — allure.step, методы snake_case без await. Удали декоратор pytest.mark.skip. Запуск из academy/python-playwright: `../../.venv/bin/python -m pytest tests/test_11_practice.py`.

Предусловия в fixtures готовы. В обоих вариантах нужны те же действия и четыре проверки, что в JS. Не превращай каждый шаг Playwright или pytest в отдельный зависимый тест.

Справочник актуальных Page Object и синтаксиса трёх стеков: [PAGE-OBJECTS.md](PAGE-OBJECTS.md).
