import json
import uuid

import allure
import httpx


class ShopApi:
    """HTTP-клиент магазина.

    Методы возвращают httpx.Response и не бросают исключений на 4xx/5xx:
    статус и тело — это и есть предмет проверки в API-тесте.
    Каждый запрос попадает в Allure шагом с телами запроса и ответа.
    """

    def __init__(self, base_url: str, token: str | None = None):
        self.http = httpx.Client(base_url=base_url + '/api', timeout=10)
        self.token = token
        self.user: dict | None = None

    def close(self) -> None:
        self.http.close()

    # Транспорт
    def request(self, method: str, path: str, *, body=None, params=None, headers=None) -> httpx.Response:
        all_headers = {**({'Authorization': f'Bearer {self.token}'} if self.token else {}), **(headers or {})}
        with allure.step(f'{method} {path}'):
            response = self.http.request(method, path, json=body, params=params, headers=all_headers)
            allure.attach(
                json.dumps({'method': method, 'url': str(response.request.url), 'body': body,
                            'headers': {k: v for k, v in all_headers.items() if k != 'Authorization'}},
                           ensure_ascii=False, indent=2),
                name='request', attachment_type=allure.attachment_type.JSON)
            allure.attach(
                json.dumps({'status': response.status_code, 'body': _body(response)}, ensure_ascii=False, indent=2),
                name=f'response {response.status_code}', attachment_type=allure.attachment_type.JSON)
        return response

    # Пользователь и сессия
    def register(self, email: str, password: str) -> httpx.Response:
        return self.request('POST', '/users', body={'email': email, 'password': password})

    def login(self, email: str, password: str) -> httpx.Response:
        response = self.request('POST', '/login', body={'email': email, 'password': password})
        if response.status_code == 200:
            self.token = response.json()['token']
            self.user = response.json()['user']
        return response

    def logout(self) -> httpx.Response:
        return self.request('POST', '/logout')

    def me(self) -> httpx.Response:
        return self.request('GET', '/me')

    def update_profile(self, name: str) -> httpx.Response:
        return self.request('PATCH', '/me', body={'name': name})

    # Каталог
    def products(self, **params) -> httpx.Response:
        return self.request('GET', '/products', params=params)

    def product(self, product_id: int) -> httpx.Response:
        return self.request('GET', f'/products/{product_id}')

    def create_product(self, **body) -> httpx.Response:
        return self.request('POST', '/admin/products', body=body)

    # Корзина и избранное
    def cart(self) -> httpx.Response:
        return self.request('GET', '/cart')

    def put_cart(self, product_id, quantity) -> httpx.Response:
        return self.request('PUT', '/cart', body={'product_id': product_id, 'quantity': quantity})

    def remove_from_cart(self, product_id: int) -> httpx.Response:
        return self.request('DELETE', f'/cart/{product_id}')

    def add_favorite(self, product_id: int) -> httpx.Response:
        return self.request('PUT', f'/favorites/{product_id}')

    def favorites(self) -> httpx.Response:
        return self.request('GET', '/favorites')

    # Заказы
    def create_order(self, address: str, coupon: str = '', key: str | None = None) -> httpx.Response:
        # Idempotency-Key — обязательный заголовок: повтор с тем же ключом не создаёт второй заказ.
        return self.request('POST', '/orders', body={'address': address, 'coupon': coupon},
                            headers={'Idempotency-Key': key or uuid.uuid4().hex})

    def orders(self) -> httpx.Response:
        return self.request('GET', '/orders')

    def order(self, order_id: int) -> httpx.Response:
        return self.request('GET', f'/orders/{order_id}')

    def pay(self, order_id: int) -> httpx.Response:
        return self.request('POST', f'/orders/{order_id}/pay')

    def cancel(self, order_id: int) -> httpx.Response:
        return self.request('POST', f'/orders/{order_id}/cancel')


def _body(response: httpx.Response):
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text
