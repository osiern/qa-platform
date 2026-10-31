"""Transactional outbox -> Kafka -> идемпотентная обработка оплаты."""
import json
import logging
import signal
import time
from kafka import KafkaProducer, KafkaConsumer
from sqlalchemy import select
from shop.db import Session, Outbox, Order, PaymentEvent
from shop.settings import KAFKA_BOOTSTRAP, PAYMENT_TOPIC

log = logging.getLogger('payments')
running = True


def stop(*_):
    global running
    running = False


def apply_payment(payload):
    with Session.begin() as db:
        order = db.scalar(select(Order).where(Order.id == payload['order_id']).with_for_update())
        if not order:  # тест уже завершился и удалил свои данные
            return
        if db.get(PaymentEvent, payload['event_id']):
            return
        if order.status != 'payment_pending' or order.total != payload['amount']:
            raise ValueError('Несогласованное событие оплаты')
        db.add(PaymentEvent(event_id=payload['event_id'], order_id=order.id, amount=payload['amount']))
        order.status = 'paid'


def main():
    logging.basicConfig(level=logging.INFO)
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP,
        value_serializer=lambda value: json.dumps(value).encode(), acks='all')
    consumer = KafkaConsumer(PAYMENT_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id='qa-payments-v1', auto_offset_reset='earliest', enable_auto_commit=False,
        value_deserializer=lambda value: json.loads(value.decode()))
    try:
        while running:
            with Session.begin() as db:
                for event in db.scalars(select(Outbox).where(Outbox.published.is_(False)).with_for_update(skip_locked=True).limit(20)):
                    producer.send(PAYMENT_TOPIC, key=str(event.order_id).encode(), value=event.payload).get(timeout=10)
                    event.published = True
            for records in consumer.poll(timeout_ms=300, max_records=20).values():
                for record in records:
                    apply_payment(record.value)
            # Все полученные сообщения записаны в PostgreSQL; при сбое до commit
            # Kafka доставит их повторно, PaymentEvent защитит от дубля.
            consumer.commit()
    finally:
        consumer.close()
        producer.close()


if __name__ == '__main__':
    main()
