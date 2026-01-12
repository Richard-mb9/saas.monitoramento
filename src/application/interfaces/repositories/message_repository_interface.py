from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from domain import Message


class MessageRepositoryInterface(ABC):

    @abstractmethod
    def insert(self, message: Message) -> Message:
        raise NotImplementedError("Should implement method: insert_if_not_exist")

    @abstractmethod
    def find_by_id(self, message_id: UUID) -> Optional[Message]:
        raise NotImplementedError("Should implement method: insert_if_not_exist")
