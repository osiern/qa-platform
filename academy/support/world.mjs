import { randomUUID } from 'node:crypto';
import pg from 'pg';
import { createClient } from 'redis';
export const baseURL = process.env.BASE_URL || 'http://127.0.0.1:8010';
export async function createWorld({ productCount = 1 } = {}) {
    const user = { email: `academy-${randomUUID()}@example.test`, password: 'Study-password-123' };
    const tokens = new Set();
    let userId, product;
    const products = [];
    const searchPrefix = `Учебный рюкзак ${randomUUID().slice(0, 8)}`;
    async function request(path, { method = 'GET', body, token } = {}) {
        const response = await fetch(new URL(path, baseURL), {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
            },
            ...(body === undefined ? {} : { body: JSON.stringify(body) }),
        });
        const text = await response.text();
        if (!response.ok) throw new Error(`${method} ${path}: ${response.status}: ${text}`);
        return text ? JSON.parse(text) : undefined;
    }
    async function cleanup(extraToken) {
        if (extraToken) tokens.add(extraToken);
        const db = new pg.Pool({
            connectionString:
                process.env.DATABASE_URL || 'postgresql://qa:qa_local_only@127.0.0.1:55432/qa_shop',
        });
        const redis = createClient({ url: process.env.REDIS_URL || 'redis://127.0.0.1:56379/0' });
        try {
            await redis.connect();
            if (userId) {
                await redis.del([`cart:${userId}`, `favorites:${userId}`]);
                // Удаляем только сессии своего пользователя, не затрагивая ручные аккаунты.
                for await (const keys of redis.scanIterator({ MATCH: 'session:*' })) {
                    for (const key of keys) {
                        if (await redis.get(key) === String(userId)) await redis.del(key);
                    }
                }
                await db.query('DELETE FROM users WHERE id=$1 AND email=$2', [userId, user.email]);
            }
            for (const created of products) await db.query('DELETE FROM products WHERE id=$1', [created.id]);
            if (tokens.size) await redis.del([...tokens].map((token) => `session:${token}`));
        } finally {
            if (redis.isOpen) await redis.quit();
            await db.end();
        }
    }
    try {
        userId = (await request('/api/users', { method: 'POST', body: user })).id;
        const admin = await request('/api/login', {
            method: 'POST',
            body: {
                email: process.env.ADMIN_EMAIL || 'admin@example.test',
                password: process.env.ADMIN_PASSWORD || 'Admin-study-123',
            },
        });
        tokens.add(admin.token);
        for (let index = 0; index < productCount; index++) {
            product = await request('/api/admin/products', {
                method: 'POST',
                token: admin.token,
                body: {
                    name: `${searchPrefix} ${index + 1}`,
                    category: 'accessories',
                    price: 123400 + index * 10000,
                    stock: 10,
                    description: 'Изолированный товар для одного упражнения',
                },
            });
            products.push(product);
        }
        product = products[0];
        return { user, product, products, searchPrefix, cleanup };
    } catch (error) {
        await cleanup();
        throw error;
    }
}
