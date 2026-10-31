# Backend and API tests

Pytest integration suite for the `qa-platform` shop. Tests use the running local Compose stand and cover HTTP API behavior, PostgreSQL persistence and constraints, Redis sessions and cart, Kafka payment processing, gRPC inventory, and key end-to-end flows.

## Run

From the `qa-platform` root, start the stand:

```sh
sh scripts/dc.sh up -d --build
```

Run the complete suite from this directory:

```sh
../../.venv/bin/python -m pytest
```

Select an area with its marker:

```sh
../../.venv/bin/python -m pytest -m api
../../.venv/bin/python -m pytest -m 'grpc or postgres or sql or redis or kafka'
../../.venv/bin/python -m pytest -m e2e
../../.venv/bin/python -m pytest -m docker
```

The stand must be healthy before running tests. Each test creates uniquely named data and removes its own records and cache keys. Allure results are written to `academy/artifacts/allure-results/backend-api-tests`.

## Coverage

| Path | Coverage |
|---|---|
| `tests/api/` | HTTP status codes, schemas, validation, authentication, authorization, catalog, cart, orders and idempotency |
| `tests/backend/database/` | SQL persistence, PostgreSQL constraints, transactions, locking, concurrent checkout and cleanup |
| `tests/backend/redis/` | Session and cart data, key types, TTL and API/cache consistency |
| `tests/backend/kafka/` | Outbox, payment events, worker processing and duplicate handling |
| `tests/backend/grpc/` | Inventory contract, authorization, error codes and database consistency |
| `tests/e2e/` | Full order and payment flow across HTTP, PostgreSQL, Redis, gRPC and Kafka |
| `tests/platform/` | Compose health, dependencies, ports, volumes, service discovery and logs |
| `clients/` | Small HTTP, SQL, Redis, Kafka, gRPC and Compose helpers shared by tests |

## Known application defects

- Product search does not escape `%` and `_` in `ILIKE`; the API test records this as a strict expected failure.
- A malformed Kafka payment event can stop the worker; the current application has no dead-letter queue.
