import json
import time

import allure
from kafka import KafkaConsumer, KafkaProducer, TopicPartition


class PaymentTopic:
    """Чтение и публикация событий оплаты в Kafka.

    Читаем без group_id: тестовый consumer не коммитит offset и не мешает
    worker (его группа qa-payments-v1). Перед действием встаём в конец топика,
    чтобы увидеть только новые сообщения.
    """

    def __init__(self, bootstrap: str, topic: str):
        self.topic = topic
        self.partition = TopicPartition(topic, 0)
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap, group_id=None, enable_auto_commit=False,
            value_deserializer=lambda value: json.loads(value.decode()),
            key_deserializer=lambda key: key.decode() if key else None,
        )
        self.consumer.assign([self.partition])
        self.bootstrap = bootstrap

    def close(self) -> None:
        self.consumer.close()

    def move_to_end(self) -> int:
        self.consumer.seek_to_end(self.partition)
        # position() выполняет отложенный seek сразу, иначе сообщения до действия могли бы прочитаться.
        return self.consumer.position(self.partition)

    def wait_for(self, order_id: int, timeout: float = 20):
        with allure.step(f'Kafka: дождаться события оплаты заказа {order_id}'):
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                for records in self.consumer.poll(timeout_ms=500).values():
                    for record in records:
                        if record.value.get('order_id') == order_id:
                            allure.attach(json.dumps({'offset': record.offset, 'key': record.key,
                                                      'value': record.value}, ensure_ascii=False, indent=2),
                                          name='kafka record', attachment_type=allure.attachment_type.JSON)
                            return record
            raise AssertionError(f'За {timeout} с событие оплаты заказа {order_id} не появилось в {self.topic}')

    def publish(self, payload: dict, key: str) -> None:
        """Повторно публикует событие. Только корректные события: см. урок 07 про poison message."""
        producer = KafkaProducer(bootstrap_servers=self.bootstrap, acks='all',
                                 value_serializer=lambda value: json.dumps(value).encode())
        try:
            with allure.step(f'Kafka: опубликовать событие {payload.get("event_id")}'):
                producer.send(self.topic, key=key.encode(), value=payload).get(timeout=10)
        finally:
            producer.close()
