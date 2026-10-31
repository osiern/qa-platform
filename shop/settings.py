import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg://qa:qa_local_only@localhost:55432/qa_shop')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:56379/0')
KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP', 'localhost:59092')
PAYMENT_TOPIC = 'qa.payment.requested.v1'
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.test')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Admin-study-123')
SESSION_TTL = 3600
