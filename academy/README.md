# Академия AQA: один магазин, три стека

В каждом стеке **10 одинаковых готовых E2E и один файл упражнений №11**. Все тестовые файлы находятся в `tests/` и пронумерованы. Тесты оформлены по шаблону рабочего проекта fleet-autotests: шапка с метаданными, `describe('Раздел: сценарий')`, константа `DATA`, шаги pre/it/auto/check, Page Object и общие шаги в `shared/`. Fixture создаёт отдельного пользователя и товары через API и удаляет свои данные после сценария.

Десятка подобрана под вопросы на собеседовании AQA:

1. Авторизация: вход, сохранение сессии после обновления и выход.
2. Авторизация: неверный пароль не открывает аккаунт.
3. Каталог: обе границы диапазона цен включены в фильтр.
4. Каталог: сортировка по возрастанию цены.
5. Каталог: пагинация без дублей и пропусков.
6. Заказы: покупка со скидкой 10% по промокоду.
7. Корзина: количество больше остатка отклоняется, корзина сохраняется.
8. Заказы: адрес короче 5 символов не создаёт заказ.
9. Оплата: асинхронная оплата переводит заказ в paid.
10. Заказы: отмена требует подтверждения и возвращает остаток.

## Стенд

Из `qa-platform`: `sh scripts/dc.sh up -d --build`.
Если Docker остановлен: `colima start qa-platform --cpu 2 --memory 4 --disk 20 --activate=false --ssh-config=false`.

- Магазин: http://127.0.0.1:8010/
- Академия: http://127.0.0.1:8010/static/academy.html
- Ещё 20 заданий: http://127.0.0.1:8010/static/scenarios.html
- Swagger: http://127.0.0.1:8010/docs

Пользователей для ручной практики можно зарегистрировать в UI. Тесты создают свои аккаунты. Все товары, заказы и оплата учебные.

## JS + WebdriverIO

Node.js 22+. Из `qa-platform/academy`:

```sh
npm ci
npm run test:js
npm run practice:js
```

Готовые: `js-wdio/tests/01-…` — `10-…`. Упражнение: `js-wdio/tests/11-practice.spec.js`.
Один describe — один E2E. pre — подготовка, it — одно действие, auto — технический шаг, check — один expect. Как в рабочем проекте, pre/check/auto — глобальные алиасы it из `beforeSession` в `wdio.conf.js`, импортировать их не нужно. Включён `bail`: после первого упавшего шага остальные не выполняются, очистка в after выполняется.
Для видимого окна: `HEADED=1 npm run test:js`. `npm run answers:js` — алиас готовой десятки, повторно запускать его после test:js не требуется.

## TS + Playwright Test

Из `qa-platform/academy`:

```sh
npm ci
npx playwright install chromium
npm run typecheck
npm run test:ts
npm run practice:ts
```

Готовые: `ts-playwright/tests/01-…` — `10-…`. Упражнение: `ts-playwright/tests/11-practice.spec.ts`.
Один test — один E2E, внутри отдельные `test.step('it: …')` и `test.step('check: …')`. После ошибки тест останавливается. Для массивов используется expect.poll, для элементов — ожидающие утверждения Playwright. У каждого теста новый browser context.
Для видимого окна: `HEADED=1 npm run test:ts`. `npm run answers:ts` — алиас готовой десятки.

## Python + Playwright + pytest

Один раз из `qa-platform`:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python -m playwright install chromium
```

Затем из `qa-platform/academy/python-playwright`:

```sh
../../.venv/bin/python -m pytest
../../.venv/bin/python -m pytest tests/test_11_practice.py
```

Готовые: `python-playwright/tests/test_01_…` — `test_10_…`. Упражнение: `tests/test_11_practice.py`.
Одна test-функция — один E2E, шаги — `with allure.step('it: …')` и `with allure.step('check: …')`. Один check содержит один expect или assert. Это sync API: await не нужен. Новый context создаётся для каждого сценария.
Для видимого окна: `HEADED=1 ../../.venv/bin/python -m pytest`.

## Backend и API + Python + pytest

Отдельный набор интеграционных тестов проверяет HTTP API и взаимодействие сервисов: PostgreSQL, Redis, Kafka, gRPC и Compose. Это не браузерный стек, и он запускается на том же локальном магазине.

Из `qa-platform` запусти стенд, затем из `academy/backend-api-tests`:

```sh
../../.venv/bin/python -m pytest
../../.venv/bin/python -m pytest -m api
../../.venv/bin/python -m pytest -m 'grpc or postgres or sql or redis or kafka'
../../.venv/bin/python -m pytest -m e2e
```

Подробный состав покрытия и команды — в [README набора](backend-api-tests/README.md).

## Page Object

Актуальные классы покрывают все разделы магазина. [Как обращаться к элементам и действиям](docs/PAGE-OBJECTS.md). В JS Page Object — один экземпляр: `import Shop from '../pages/ShopPage.js'`, элементы `Shop.identity` и `Shop.cartRow(id)`. В TS — `shop.identity` и `shop.cartRow(id)`. В Python — `shop.identity` и `shop.cart_row(id)`.

## Общие шаги

Вход, поиск своих товаров, добавление в корзину и оформление заказа вынесены в `shared/` каждого стека: `login`, `searchOwnProducts`, `addProductToCart`, `placeOrder`. Хелпер регистрирует те же шаги, что были бы в тесте. Подробности — в [PAGE-OBJECTS.md](docs/PAGE-OBJECTS.md#общие-шаги-shared).

## Упражнение 11

Один сценарий покупки без промокода с готовой API-подготовкой. Заполни TODO, убери skip у сценария и запусти команду practice. Пока skip не снят, упражнение пропущено, а не пройдено. Без заполнения TODO шаги намеренно падают. [Пошаговый урок](docs/LESSON-01.md).

## Отчёты и проверки

Из academy: `npm run typecheck`, `npm run report` (HTML Playwright), `npm run allure:generate`, `npm run allure:open`.
Python сохраняет Allure в academy/artifacts/allure-results/python, JS и TS — в соседних каталогах js и ts. На падении TS сохраняет screenshot и trace; Python прикладывает их к Allure и сохраняет trace в artifacts/python-traces. В Allure 3 используется Node.js, отдельная Java не нужна.

Workflow `.github/workflows/academy.yml` запускает JS, TS и Python по одному разу и сохраняет артефакты. Удалённый запуск нужно выполнить в своём GitHub-репозитории; наличие workflow не доказывает успешный CI.

## Что изучать дальше

[Кейсы и ожидаемые результаты](docs/CASES.md) · [Вопросы для собеседования](docs/INTERVIEW-E2E.md) · [Маршрут всего стека](docs/ROADMAP.md).

Набор `backend-api-tests` уже проверяет API, PostgreSQL, Redis, Kafka, gRPC и базовое состояние Compose. Нагрузочное тестирование, accessibility и проверки миграций остаются за его пределами.

Локальный запуск рассчитан на BASE_URL=http://127.0.0.1:8010 и связанные PostgreSQL/Redis из compose. Для другого стенда нужно согласованно настроить BASE_URL, DATABASE_URL и REDIS_URL. Очистка затрагивает только созданные тестом записи и сессии своего пользователя.
