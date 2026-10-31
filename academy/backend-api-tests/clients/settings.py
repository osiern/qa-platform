import os
from pathlib import Path

# Корень qa-platform: отсюда импортируются gRPC-стабы shop.proto и запускается scripts/dc.sh.
ROOT = Path(__file__).resolve().parents[3]

BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8010')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://qa:qa_local_only@127.0.0.1:55432/qa_shop')
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:56379/0')
KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP', '127.0.0.1:59092')
GRPC_TARGET = os.getenv('GRPC_TARGET', '127.0.0.1:50051')
PAYMENT_TOPIC = 'qa.payment.requested.v1'
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.test')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Admin-study-123')
SESSION_TTL = 3600
CART_TTL = 86400
