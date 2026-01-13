from uuid import UUID
from typing import Optional
from json import dumps
from pika.adapters.blocking_connection import BlockingChannel
from pika import (
    BlockingConnection,
    BasicProperties,
    PlainCredentials,
    ConnectionParameters,
)

from application.interfaces import PublisherInterface
from config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    RABBITMQ_QUEUE_NEW_MESSAGE,
)


class RabbitMQPublisher(PublisherInterface):
    _channel: Optional[BlockingChannel]
    _connection: Optional[BlockingConnection]

    def __init__(self, topic_name: str = "message"):
        self._connection = BlockingConnection(
            ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
            )
        )
        self._topic_name = topic_name
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=self._topic_name, exchange_type="topic", durable=True
        )

    def publish_new_message(self, message_id: UUID):
        try:
            payload = dumps({"message_id": str(message_id)})
            result = self.__publish(payload)
            if result is True:
                print(f"[RabbitMQ] Evento new_message publicado: {message_id}")
                return
            print(f"[RabbitMQ] Erro ao publicar o evento da mensagem: {message_id}")
        except Exception as e:
            print(f"[RabbitMQ] Erro ao publicar evento: {e}")
            # Força reconexão na próxima tentativa
            self._connection = None
            self._channel = None

    def close(self):
        if self._channel and self._channel.is_open:
            self._channel.close()
        if self._connection and self._connection.is_open:
            self._connection.close()

    def __publish(self, payload: str) -> bool:
        if self._connection and self._channel:
            self._channel.basic_publish(
                exchange=self._topic_name,
                routing_key=RABBITMQ_QUEUE_NEW_MESSAGE,
                body=payload,
                properties=BasicProperties(
                    delivery_mode=2,  # Mensagem persistente
                    content_type="application/json",
                ),
            )
            return True
        return False
