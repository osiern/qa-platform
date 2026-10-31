import { existsSync, readFileSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { spawnSync } from 'node:child_process';

// Allure reads each explicitly named results directory; do not pass their empty parent.
const directories = ['js', 'ts', 'python', 'backend-api-tests']
    .map((name) => resolve('artifacts/allure-results', name))
    .filter(existsSync);
if (!directories.length) {
    console.error('Сначала запусти готовые примеры: результатов Allure пока нет.');
    process.exit(1);
}
const packageRoot = resolve('node_modules/allure');
const meta = JSON.parse(readFileSync(join(packageRoot, 'package.json'), 'utf8'));
const cli = join(packageRoot, typeof meta.bin === 'string' ? meta.bin : meta.bin.allure);
const result = spawnSync(
    process.execPath,
    [cli, 'generate', ...directories, '--output', resolve('artifacts/allure-report'), '--clean'],
    { stdio: 'inherit' },
);
process.exit(result.status ?? 1);
