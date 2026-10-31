import { fileURLToPath } from 'node:url';
import { defineConfig } from '@playwright/test';
export default defineConfig({
    testDir: './tests',
    testMatch: '**/*.spec.ts',
    fullyParallel: true,
    workers: 1,
    timeout: 30000,
    expect: { timeout: 10000 },
    outputDir: '../artifacts/ts-results',
    reporter: [
        ['list'],
        [
            'html',
            {
                outputFolder: fileURLToPath(
                    new URL('../artifacts/playwright-report', import.meta.url),
                ),
                open: 'never',
            },
        ],
        [
            'allure-playwright',
            {
                resultsDir: fileURLToPath(
                    new URL('../artifacts/allure-results/ts', import.meta.url),
                ),
            },
        ],
    ],
    use: {
        baseURL: process.env.BASE_URL || 'http://127.0.0.1:8010',
        headless: process.env.HEADED !== '1',
        viewport: { width: 1280, height: 900 },
        trace: 'retain-on-failure',
        screenshot: 'only-on-failure',
    },
});
