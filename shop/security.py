import hashlib
import hmac
import secrets
from redis import Redis
from shop.settings import REDIS_URL

cache = Redis.from_url(REDIS_URL, decode_responses=True)


def hash_password(password):
    salt = secrets.token_hex(16)
    value = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 200_000)
    return salt + ':' + value.hex()


def verify_password(password, encoded):
    salt, expected = encoded.split(':')
    actual = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 200_000).hex()
    return hmac.compare_digest(expected, actual)


def session_user(token):
    uid = cache.get('session:' + token) if token else None
    return int(uid) if uid else None
