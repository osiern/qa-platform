import allure
import redis


class Cache:
    """Redis магазина.

    Ключи:
      session:{token}   → id пользователя, TTL 3600 с
      cart:{user_id}    → hash product_id → количество, TTL 86400 с
      favorites:{user_id} → set id товаров, без TTL
    """

    def __init__(self, url: str):
        self.redis = redis.Redis.from_url(url, decode_responses=True)

    def close(self) -> None:
        self.redis.close()

    def get(self, key: str) -> str | None:
        with allure.step(f'Redis GET {key[:40]}'):
            return self.redis.get(key)

    def ttl(self, key: str) -> int:
        # -2 — ключа нет, -1 — ключ без срока жизни, иначе секунды до удаления.
        with allure.step(f'Redis TTL {key[:40]}'):
            return self.redis.ttl(key)

    def type(self, key: str) -> str:
        return self.redis.type(key)

    def hgetall(self, key: str) -> dict:
        with allure.step(f'Redis HGETALL {key}'):
            return self.redis.hgetall(key)

    def smembers(self, key: str) -> set:
        with allure.step(f'Redis SMEMBERS {key}'):
            return self.redis.smembers(key)

    def exists(self, key: str) -> bool:
        return bool(self.redis.exists(key))

    def delete_user_data(self, user_id: int) -> None:
        """Удаляет только ключи одного пользователя. FLUSHDB на общем стенде запрещён."""
        self.redis.delete(f'cart:{user_id}', f'favorites:{user_id}')
        for key in self.redis.scan_iter(match='session:*', count=500):
            if self.redis.get(key) == str(user_id):
                self.redis.delete(key)
