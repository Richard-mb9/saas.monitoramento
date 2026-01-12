from abc import ABC, abstractmethod

from domain import Message


class MessageRepositoryInterface(ABC):

    @abstractmethod
    def insert(self, message: Message) -> Message:
        raise NotImplementedError("Should implement method: insert")
