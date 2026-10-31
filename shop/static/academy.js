const tracks = {
  js: {
    title: "JavaScript + WebdriverIO",
    folder: "js-wdio",
    start: "npm run test:js",
    practice: "npm run practice:js",
    file: "11-practice.spec.js",
    cwd: "qa-platform/academy",
    setup: "npm ci",
    syntax:
      "it('Ввести email', async () => { await Shop.enterEmail(world.user.email); });\ncheck('Email виден', async () => { await expect(Shop.identity).toHaveText(world.user.email); });",
    rules:
      "В файле один describe — один E2E, оформленный по шаблону рабочего проекта: метаданные в шапке, DATA, общие шаги из shared/. pre, it, auto и check регистрируют отдельные шаги Mocha; после упавшего шага остальные не выполняются (bail).",
  },
  ts: {
    title: "TypeScript + Playwright Test",
    folder: "ts-playwright",
    start: "npm run typecheck\nnpm run test:ts",
    practice: "npm run practice:ts",
    file: "11-practice.spec.ts",
    cwd: "qa-platform/academy",
    setup: "npm ci\nnpx playwright install chromium",
    syntax:
      "await test.step('it: Ввести email', async () => { await shop.enterEmail(world.user.email); });\nawait test.step('check: Email виден', async () => { await expect(shop.identity).toHaveText(world.user.email); });",
    rules:
      "В файле один test. Действия и проверки разделены test.step. Каждый check содержит один expect. У каждого E2E свой browser context; после ошибки дальнейшие шаги не исполняются.",
  },
  py: {
    title: "Python + Playwright + pytest",
    folder: "python-playwright",
    start: "../../.venv/bin/python -m pytest",
    practice: "../../.venv/bin/python -m pytest tests/test_11_practice.py",
    file: "test_11_practice.py",
    cwd: "qa-platform/academy/python-playwright",
    setup:
      "Из qa-platform:\npython3 -m venv .venv\n.venv/bin/python -m pip install -r requirements.lock.txt\n.venv/bin/python -m playwright install chromium",
    syntax:
      "with allure.step('it: Ввести email'):\n    shop.enter_email(world['user']['email'])\nwith allure.step('check: Email виден'):\n    expect(shop.identity).to_have_text(world['user']['email'])",
    rules:
      "В файле одна test-функция pytest. Шаги оформлены with allure.step. Один check — один expect или assert. Используется sync API: await здесь не нужен.",
  },
};
let selected = "js";
let done = {};
try {
  const value = JSON.parse(localStorage.getItem("academy-progress-v2") || "{}");
  if (value && typeof value === "object" && !Array.isArray(value)) done = value;
} catch {}
function node(tag, text, cls) {
  const element = document.createElement(tag);
  if (text) element.textContent = text;
  if (cls) element.className = cls;
  return element;
}
function updateProgress() {
  const total = Object.keys(tracks).reduce(
    (sum, key) =>
      sum + cases.filter((item) => done[key + item.id] === true).length,
    0,
  );
  document.querySelector("#progress").textContent = `Разобрано: ${total} / 30`;
}
function list(items) {
  const el = node("ol", null, "case-list");
  for (const text of items) el.append(node("li", text));
  return el;
}
function render() {
  const content = document.querySelector("#content");
  content.replaceChildren();
  document
    .querySelectorAll("[data-track]")
    .forEach((button) =>
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.track === selected),
      ),
    );
  updateProgress();
  if (selected === "advanced") {
    content.append(
      node("h2", "Backend и API"),
      node(
        "p",
        "Здесь собраны интеграционные автотесты на Python и pytest. Они проверяют HTTP API и работу PostgreSQL, Redis, Kafka и gRPC на локальном Docker Compose стенде.",
      ),
    );
    const card = node("article", null, "card");
    card.append(
      list([
        "HTTP / REST: статусы и схемы ответов, валидация, авторизация, каталог, корзина, заказы и Idempotency-Key.",
        "PostgreSQL: сохранение данных, ограничения, транзакции, блокировки и гонка при покупке последнего товара.",
        "Redis: сессии и корзина, типы ключей, TTL и согласованность с ответами API.",
        "gRPC: контракт Inventory, авторизация, коды ошибок и сверка остатков с PostgreSQL.",
        "Kafka: outbox, событие оплаты, обработка worker и повторная доставка.",
        "Сквозной сценарий: заказ проходит через HTTP, PostgreSQL, Redis, gRPC, Kafka и worker.",
        "Docker Compose: healthcheck, зависимости, порты, тома, service discovery и логи.",
        "Allure и GitHub Actions: отчёт по шагам и запуск набора в CI.",
      ]),
    );
    content.append(card);
    content.append(
      node("h3", "Запуск"),
      node("p", "Из корня проекта сначала подними стенд: sh scripts/dc.sh up -d --build"),
      node("pre", "cd academy/backend-api-tests\n../../.venv/bin/python -m pytest"),
    );
    const link = node("a", "Открыть Swagger");
    link.href = "/docs";
    const testsLink = node("a", "Открыть backend/API-тесты на GitHub");
    testsLink.href = "https://github.com/osiern/qa-platform/tree/main/academy/backend-api-tests";
    testsLink.target = "_blank";
    testsLink.rel = "noopener noreferrer";
    content.append(
      link,
      document.createTextNode(" · "),
      testsLink,
      node(
        "p",
        "Полный маршрут: academy/docs/ROADMAP.md. Дополнительные UI-сценарии — по ссылке «Ещё 20 заданий» вверху.",
      ),
    );
    return;
  }
  const track = tracks[selected];
  content.append(node("h2", track.title), node("p", track.rules));
  const pom = node("details");
  const pomFile =
    selected === "py"
      ? "python-playwright/pages/shop_page.py"
      : track.folder + "/pages/ShopPage." + (selected === "js" ? "js" : "ts");
  const pomSyntax =
    selected === "js"
      ? "await Shop.enterEmail(world.user.email);\nawait expect(Shop.identity).toHaveText(world.user.email);\nawait expect(Shop.cartRow(world.product.id)).toBeDisplayed();"
      : selected === "ts"
        ? "await shop.enterEmail(world.user.email);\nawait expect(shop.identity).toHaveText(world.user.email);\nawait expect(shop.cartRow(world.product.id)).toBeVisible();"
        : "shop.enter_email(world['user']['email'])\nexpect(shop.identity).to_have_text(world['user']['email'])\nexpect(shop.cart_row(world['product']['id'])).to_be_visible()";
  pom.append(
    node("summary", "Page Object: элементы и действия"),
    node("p", "Файл: " + pomFile),
    node(
      "p",
      "Метод выполняет действие, именованный локатор возвращает элемент для проверки. Классы покрывают авторизацию, каталог, фильтры, избранное, окно товара, корзину, заказы и профиль. Полный справочник: academy/docs/PAGE-OBJECTS.md.",
    ),
    node("pre", pomSyntax),
  );
  content.append(pom);

  const term = node("div", null, "terminal");
  term.append(
    node("strong", "10 готовых E2E + 1 упражнение"),
    node(
      "p",
      "Рабочая папка: " +
        track.cwd +
        ". Магазин должен работать на http://127.0.0.1:8010.",
    ),
    node("p", "Установка зависимостей один раз:"),
    node("pre", track.setup),
    node("p", "Запуск готовых сценариев:"),
    node("pre", track.start),
  );
  const copy = node("button", "Скопировать команду запуска", "copy");
  copy.onclick = async () => {
    try {
      await navigator.clipboard.writeText(track.start);
      copy.textContent = "Скопировано";
    } catch {
      copy.textContent = "Выдели команду выше";
    }
  };
  term.append(copy);
  term.append(
    node("p", "Упражнение: " + track.folder + "/tests/" + track.file),
    node("pre", track.practice),
    node(
      "p",
      "В упражнении покупка без промокода. Замени TODO на действия и проверки, затем убери skip. До этого упражнение пропущено, а не пройдено. Ожидаются: товар в корзине, верная сумма, статус new и сумма заказа без скидки.",
    ),
  );
  content.append(term);
  const example = node("details");
  example.append(
    node("summary", "Как оформляются действия и проверки"),
    node("pre", track.syntax),
  );
  content.append(example);
  const search = node("input", null, "case-search");
  search.type = "search";
  search.placeholder = "Найти сценарий или тему";
  search.setAttribute("aria-label", "Поиск по учебным сценариям");
  content.append(search);
  const count = node("p", "10 сценариев", "status-line");
  count.setAttribute("role", "status");
  content.append(count);
  const container = node("div");
  content.append(container);
  function draw() {
    container.replaceChildren();
    const query = search.value.trim().toLocaleLowerCase("ru");
    const visible = cases.filter((item) =>
      (item.title + " " + item.topic).toLocaleLowerCase("ru").includes(query),
    );
    count.textContent = "Сценариев: " + visible.length + " из 10";
    for (const item of visible) {
      const card = node("article", null, "card");
      const meta = node("div", null, "meta");
      const heading = node("div");
      heading.append(
        node("div", "E2E " + item.id, "id"),
        node("h3", item.title),
      );
      const label = node("label");
      const checkbox = node("input");
      checkbox.type = "checkbox";
      checkbox.checked = done[selected + item.id] === true;
      checkbox.setAttribute(
        "aria-label",
        "Я разобрал сценарий " + item.id + " на " + track.title,
      );
      checkbox.onchange = () => {
        done[selected + item.id] = checkbox.checked;
        try {
          localStorage.setItem("academy-progress-v2", JSON.stringify(done));
        } catch {}
        updateProgress();
      };
      label.append(checkbox, document.createTextNode(" Разобрал сам"));
      meta.append(heading, label);
      card.append(
        meta,
        node("p", "Файл: " + track.folder + "/tests/" + item[selected]),
        node("p", "Предусловия: " + item.pre),
      );
      const steps = node("details");
      steps.append(
        node("summary", "Действия пользователя (" + item.actions.length + ")"),
        list(item.actions),
      );
      card.append(steps);
      const checks = node("details");
      checks.append(
        node("summary", "Ожидаемые результаты (" + item.expected.length + ")"),
        list(item.expected),
      );
      card.append(checks);
      const topic = node("details");
      topic.append(
        node("summary", "Что уметь объяснить на собеседовании"),
        node("p", item.topic),
        node(
          "p",
          "Объясни выбор UI-проверки, подготовку данных, ожидания и очистку. Сравни тот же номер файла на других языках. Полные пояснения: academy/docs/INTERVIEW-E2E.md.",
        ),
      );
      card.append(topic);
      container.append(card);
    }
  }
  search.oninput = draw;
  draw();
  content.append(
    node(
      "p",
      "Рекомендуемый порядок: JS → TS → Python. Номера 01–10 обозначают одинаковые бизнес-сценарии во всех трёх стеках. Дополнительные 20 заданий не входят в готовую десятку.",
      "notice",
    ),
  );
}
document.querySelectorAll("[data-track]").forEach(
  (button) =>
    (button.onclick = () => {
      selected = button.dataset.track;
      render();
    }),
);
render();
