# Page Object текущего магазина

Page Object — это класс, в котором мы называем элементы страницы и описываем действия с ними. В тесте остаются сценарий и проверки. Если у поля изменится селектор, исправляем его в Page Object, а не во всех тестах.

## Где лежит

| Стек | Файл | Как получить |
|---|---|---|
| JS + WebdriverIO | `js-wdio/pages/ShopPage.js` | `import Shop from '../pages/ShopPage.js'` — один экземпляр, как в рабочем проекте |
| TS + Playwright | `ts-playwright/pages/ShopPage.ts` | `shop` из fixture |
| Python + Playwright | `python-playwright/pages/shop_page.py` | `shop` из pytest fixture |

В каждом классе элементы сгруппированы по разделам магазина. Все три класса предоставляют одинаковые возможности. В Python имена записаны в snake_case.

## Элемент, действие, проверка

JS устроен как Page Object рабочего проекта: класс экспортируется одним экземпляром, элемент — геттер, действие — async-метод.

```javascript
get emailInput() {
    return $('[name="email"]');
}

async enterEmail(email) {
    await this.emailInput.setValue(email);
}

export default new ShopPage();
```

Геттер читается без скобок: `Shop.emailInput`. WebdriverIO ищет элемент заново при каждом обращении, поэтому после перерисовки страницы ссылка не устаревает. Элемент конкретной записи — обычный метод с ID: `Shop.cartRow(id)`. Готовая проверка:

```javascript
await expect(Shop.identity).toHaveText(world.user.email);
await expect(Shop.cartRow(world.product.id)).toBeDisplayed();
```

TS возвращает стандартный Playwright Locator. Он сам ищет элемент при выполнении команды:

```typescript
get emailInput(): Locator {
    return this.page.getByLabel('Email', { exact: true });
}

async enterEmail(email: string) {
    await this.emailInput.fill(email);
}

// В test.step:
await expect(shop.identity).toHaveText(world.user.email);
await expect(shop.cartRow(world.product.id)).toBeVisible();
```

В Python `@property` возвращает такой же Locator, действия синхронные:

```python
@property
def email_input(self) -> Locator:
    return self.page.get_by_label('Email', exact=True)

def enter_email(self, email: str) -> None:
    self.email_input.fill(email)

# В allure.step:
expect(shop.identity).to_have_text(world['user']['email'])
expect(shop.cart_row(world['product']['id'])).to_be_visible()
```

## Какие действия уже есть

| Раздел | JS / TS | Python |
|---|---|---|
| Вход | enterEmail, enterPassword, submitLogin, register, logout | enter_email, enter_password, submit_login, register, logout |
| Показ пароля | setPasswordVisible(true) | set_password_visible(True) |
| Навигация | openCatalog, openCart, openOrders, openProfile | open_catalog, open_cart, open_orders, open_profile |
| Поиск | enterSearch, submitSearch | enter_search, submit_search |
| Категория и цена | selectCategory, enterMinPrice, enterMaxPrice | select_category, enter_min_price, enter_max_price |
| Наличие и избранное | setOnlyInStock, setOnlyFavorites | set_only_in_stock, set_only_favorites |
| Сортировка и сброс | sortProductsByPriceAscending, sortProductsByPriceDescending, resetFilters | sort_products_by_price_ascending, sort_products_by_price_descending, reset_filters |
| Страницы | selectPageSize, nextPage, previousPage | select_page_size, next_page, previous_page |
| Окно товара | openProductDetails, closeProductDetails, closeProductDetailsWithEscape | open_product_details, close_product_details, close_product_details_with_escape |
| Избранное товара | addToFavorites, removeFromFavorites | add_to_favorites, remove_from_favorites |
| Корзина | addToCart, removeFromCart, changeQuantity | add_to_cart, remove_from_cart, change_quantity |
| Промокод и заказ | enterCoupon, applyCoupon, enterAddress, submitOrder | enter_coupon, apply_coupon, enter_address, submit_order |
| Заказы | filterOrdersByStatus, refreshOrders, requestCancellation, keepOrder, confirmCancellation, payOrder | filter_orders_by_status, refresh_orders, request_cancellation, keep_order, confirm_cancellation, pay_order |
| Профиль | enterProfileName, saveProfile | enter_profile_name, save_profile |

Не все эти действия входят в готовую десятку: дополнительные методы нужны для 20 заданий со страницы «Что проверить».

## Как проверять результат

Для каждой проверки бери соответствующий именованный элемент: message, identity, filterError, catalogCount, detailsName, detailsImage, cartTotal, discountTotal, addressError, orderStatus, orderTotal, profileNameInput, profileError. В JS и TS используй свойство без скобок. В Python используй snake_case-свойство.

Параметризованные элементы: product(id), productName(id), productImage(id), productStock(id), cartRow(id), quantityInput(id), orderById(id), orderStatusFor(id), orderTotalFor(id). Во всех трёх стеках достаточно одной пары скобок с ID.

Если заказ один, готовые сценарии используют orderStatus/orderTotal. Если заказов несколько, укажи ID: `shop.orderStatusFor(orderId)` / `shop.order_status_for(order_id)`. Для отмены и оплаты тоже можно передать ID. Не выбирай случайный заказ первым элементом списка.

Цена в фильтре задаётся в рублях: enterMinPrice(1234). Атрибуты data-cents в корзине и заказе хранят копейки: 123400. Значения категории: accessories, screens, computers, audio; пустая строка сбрасывает категорию. Статусы фильтра заказов: new, paid, cancelled; пустая строка показывает все.

## Ожидания и границы ответственности

- Один метод действия выполняет одно логическое действие. Ввод email, ввод пароля и нажатие Войти остаются разными шагами.
- Page Object хранит селекторы только в именованных элементах. Методы используют их повторно.
- open/refresh ждут готовность страницы. waitForProductIds ждёт точный набор ID; при перерисовке сначала проверяется число карточек.
- waitForOrderStatus(status) / wait_for_order_status(status) нажимает «Обновить заказы», пока заказ не получит статус. Нужен для асинхронной оплаты: worker обрабатывает событие из Kafka не мгновенно.
- Бизнес-проверки суммы, статуса и ошибок остаются в check. Ожидающие утверждения внутри технического waitForProductIds служат только синхронизации.
- API-подготовка и очистка остаются в fixtures (JS — `shared/prepareWorld.js`), а не в Page Object.
- В тестах не используй $, locator, getByRole, evaluate или поиск DOM. Если нужного элемента нет, добавь его в соответствующий Page Object.

## Общие шаги (shared)

Повторяющиеся цепочки шагов вынесены в `shared/`, как в рабочем проекте (`fillRequiredFields`, `createAccount`). Хелпер не прячет проверки сценария: он регистрирует те же it/check, что были бы в тесте, и одинаково называется во всех стеках.

| Хелпер | Что делает | JS | TS | Python |
|---|---|---|---|---|
| prepareWorld | pre: пользователь и товары через API, after: очистка | `prepareWorld({ productCount })` | fixture `world`, `test.use({ productCount })` | fixture `world`, `parametrize('product_count', ...)` |
| openShop | pre: открыть магазин | `openShop()` | `openShop(shop)` | `open_shop(shop)` |
| login | it email, it пароль, it «Войти», check email в шапке | `login(world)` | `login(shop, world)` | `login(shop, world)` |
| searchOwnProducts | it поиск, it «Найти», auto дождаться своих товаров | `searchOwnProducts(world, { all })` | `searchOwnProducts(shop, world, { all })` | `search_own_products(shop, world, all_products=...)` |
| addProductToCart | it «В корзину», check подтверждение, it открыть корзину, check строка | `addProductToCart(world)` | `addProductToCart(shop, world)` | `add_product_to_cart(shop, world)` |
| placeOrder | it адрес, it «Оформить заказ», check статус new | `placeOrder(address)` | `placeOrder(shop, address)` | `place_order(shop, address)` |

В JS хелпер вызывается прямо в `describe` и только регистрирует шаги. Поэтому `world` читается внутри шагов, а не при вызове: объект заполняется в pre. В TS и Python хелпер — обычная функция с `test.step` / `allure.step`, она выполняется сразу.

В упражнении 11 общие шаги намеренно не используются: вход и корзину пишешь сама/сам.
