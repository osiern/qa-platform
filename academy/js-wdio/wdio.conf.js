import { fileURLToPath } from 'node:url';
const file = (path) => fileURLToPath(new URL(path, import.meta.url));
export const config = {
    runner: 'local',
    specs: [file('./tests/0[1-9]-*.spec.js'), file('./tests/10-*.spec.js')],
    maxInstances: 1,
    baseUrl: process.env.BASE_URL || 'http://127.0.0.1:8010',
    capabilities: [
        {
            browserName: 'chrome',
            'wdio:enforceWebDriverClassic': true,
            'goog:chromeOptions': {
                args:
                    process.env.HEADED === '1'
                        ? ['--window-size=1280,900']
                        : ['--headless=new', '--window-size=1280,900'],
            },
        },
    ],
    framework: 'mocha',
    // bail: после первого упавшего шага остальные не выполняются, after с очисткой — да.
    mochaOpts: { timeout: 60000, bail: true },
    logLevel: 'error',
    waitforTimeout: 10000,
    reporters: ['spec', ['allure', { outputDir: file('../artifacts/allure-results/js') }]],
    beforeSession() {
        // Как в рабочем проекте: pre, check и auto — алиасы it.
        // pre — подготовка, it — действие пользователя, check — одна проверка,
        // auto — техническое ожидание. Каждый вызов регистрирует отдельный шаг Mocha.
        for (const alias of ['pre', 'check', 'auto']) {
            globalThis[alias] = (...args) => globalThis.it(...args);
        }
    },
    beforeCommand: async function () {
        const delay = Number(process.env.SLOW_MO || 0);
        if (delay) await new Promise((resolve) => setTimeout(resolve, delay));
    },
};
