from abc import ABC, abstractmethod
from uuid import UUID


class PublisherInterface(ABC):

    @abstractmethod
    def publish_new_message(self, message_id: UUID) -> None:
        raise NotImplementedError("Should implement method: publish_new_message")
