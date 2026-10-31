import os
from pathlib import Path
from uuid import uuid4

import allure
import httpx
import psycopg
import pytest
import redis
from playwright.sync_api import sync_playwright
from pages.shop_page import ShopPage

ROOT = Path(__file__).resolve().parents[2]
BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8010')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://qa:qa_local_only@127.0.0.1:55432/qa_shop')
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:56379/0')


def api_request(path, method='GET', body=None, token=None):
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    response = httpx.request(method, f'{BASE_URL}/api{path}', json=body, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json() if response.content else None


@pytest.fixture(scope='session')
def academy_browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=os.getenv('HEADED') != '1')
        yield browser
        browser.close()


@pytest.fixture
def product_count(request):
    return getattr(request, 'param', 1)


@pytest.fixture
def world(product_count):
    user = {'email': f'academy-{uuid4().hex}@example.test', 'password': 'Study-password-123'}
    user_id = None
    products, tokens = [], []
    prefix = f'Учебный рюкзак {uuid4().hex[:8]}'
    try:
        with allure.step('pre: создать пользователя и товары через API'):
            user_id = api_request('/users', 'POST', user)['id']
            admin = api_request('/login', 'POST', {
                'email': os.getenv('ADMIN_EMAIL', 'admin@example.test'),
                'password': os.getenv('ADMIN_PASSWORD', 'Admin-study-123'),
            })
            tokens.append(admin['token'])
            for index in range(product_count):
                products.append(api_request('/admin/products', 'POST', {
                    'name': f'{prefix} {index + 1}', 'category': 'accessories',
                    'price': 123400 + index * 10000, 'stock': 10,
                    'description': 'Изолированный товар для одного сценария',
                }, admin['token']))
        yield {'user': user, 'product': products[0], 'products': products, 'searchPrefix': prefix}
    finally:
        store = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        try:
            if user_id is not None:
                store.delete(f'cart:{user_id}', f'favorites:{user_id}')
                for key in store.scan_iter(match='session:*'):
                    if store.get(key) == str(user_id):
                        store.delete(key)
            if tokens:
                store.delete(*(f'session:{token}' for token in tokens))
        finally:
            store.close()
        with psycopg.connect(DATABASE_URL) as connection:
            if user_id is not None:
                connection.execute('DELETE FROM users WHERE id=%s AND email=%s', (user_id, user['email']))
            for product in products:
                connection.execute('DELETE FROM products WHERE id=%s', (product['id'],))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, 'rep_' + report.when, report)


@pytest.fixture
def page(academy_browser, world, request):
    context = academy_browser.new_context(viewport={'width': 1280, 'height': 900})
    context.tracing.start(screenshots=True, snapshots=True)
    page = context.new_page()
    try:
        yield page
    finally:
        failed = any(getattr(request.node, 'rep_' + phase, None) and
                     getattr(request.node, 'rep_' + phase).failed for phase in ('setup', 'call'))
        if failed:
            output = ROOT / 'academy/artifacts/python-traces'
            output.mkdir(parents=True, exist_ok=True)
            artifact = output / f'{uuid4().hex}.zip'
            allure.attach(page.screenshot(), name='Ошибка UI', attachment_type=allure.attachment_type.PNG)
            context.tracing.stop(path=str(artifact))
            allure.attach.file(str(artifact), name='Playwright trace', extension='zip')
        else:
            context.tracing.stop()
        context.close()


@pytest.fixture
def shop(page):
    return ShopPage(page, BASE_URL)
