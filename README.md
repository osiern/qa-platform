# QA Platform

Учебный e-commerce проект для практики автоматизации тестирования. В репозитории находятся приложение магазина, локальный стенд на Docker Compose, UI-тесты на JavaScript/TypeScript/Python и Python-набор интеграционных тестов API и backend-сервисов.

## Что проверяется

- **UI:** сценарии магазина на WebdriverIO, Playwright Test и Python Playwright.
- **HTTP API:** контракты, валидация, авторизация, каталог, корзина, заказы и идемпотентность.
- **Backend-интеграции:** PostgreSQL, Redis, Kafka, worker и gRPC.
- **Сквозной сценарий:** заказ проходит от HTTP-запросов до асинхронной оплаты.

Приложение — демонстрационный магазин QA Market. Тестовый стенд не предназначен для production.

## Требования

- Docker Compose
- Python 3.12+
- Node.js 22+ для UI-тестов и отчётов

## Быстрый старт

Из корня проекта подними локальные сервисы:

```sh
sh scripts/dc.sh up -d --build
```

Проверить готовность магазина можно по адресу [http://127.0.0.1:8010/health](http://127.0.0.1:8010/health), Swagger UI доступен на [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs).

## Backend и API тесты

Установи Python-зависимости из корня проекта:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
```

Запусти полный интеграционный набор:

```sh
cd academy/backend-api-tests
../../.venv/bin/python -m pytest
```

Запуск по областям:

```sh
../../.venv/bin/python -m pytest -m api
../../.venv/bin/python -m pytest -m 'grpc or postgres or sql or redis or kafka'
../../.venv/bin/python -m pytest -m e2e
```

Подробнее о покрытии и расположении тестов — в [README набора](academy/backend-api-tests/README.md).

## UI тесты

Инструкции для JS/WebdriverIO, TypeScript/Playwright и Python/Playwright находятся в [academy/README.md](academy/README.md). Для JS и TypeScript установи зависимости из `academy`:

```sh
cd academy
npm ci
npx playwright install chromium
```

## Allure отчёт

После тестов собери и открой Allure-отчёт из папки `academy`:

```sh
npm run allure:generate
npm run allure:open
```

Результаты pytest сохраняются в `academy/artifacts/allure-results/backend-api-tests`.

## Структура

```text
shop/                         FastAPI-приложение и backend-сервисы
academy/backend-api-tests/    API и backend интеграционные тесты
academy/python-playwright/    Python UI-тесты
academy/js-wdio/              JavaScript UI-тесты
academy/ts-playwright/        TypeScript UI-тесты
compose.yaml                  Локальный магазин и зависимости
.github/workflows/            CI workflow
```

Остановить локальный стенд из корня проекта:

```sh
sh scripts/dc.sh down
```
