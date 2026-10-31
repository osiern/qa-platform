import { createWorld } from '../../support/world.mjs';

/**
 * Регистрирует подготовку данных через API и очистку после сценария.
 * Возвращает объект сразу, а заполняет его в шаге pre — как createServiceInAccount
 * в рабочем проекте. Поэтому поля world читаются только внутри шагов.
 *
 * @param {{productCount?: number}} [options]
 * @returns {import('../../support/world.mjs').World}
 */
export default function prepareWorld({ productCount = 1 } = {}) {
    const world = {};

    pre(`Создать пользователя и товары (${productCount} шт.) через API`, async () => {
        Object.assign(world, await createWorld({ productCount }));
    });

    after(async () => {
        if (world.cleanup) await world.cleanup();
    });

    return world;
}
