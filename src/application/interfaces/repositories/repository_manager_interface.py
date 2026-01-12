from abc import ABC, abstractmethod


from .message_repository_interface import MessageRepositoryInterface
from .chave_compra_repository_interface import ChaveCompraRepositoryInterface


class RepositoryManagerInterface(ABC):

    @abstractmethod
    def message_repository(self) -> MessageRepositoryInterface:
        raise NotImplementedError("Should implement method: message_repository")

    @abstractmethod
    def chave_compra_repository(self) -> ChaveCompraRepositoryInterface:
        raise NotImplementedError("Should implement method: chave_compra_repository")
