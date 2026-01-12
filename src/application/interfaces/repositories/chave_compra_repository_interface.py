from abc import ABC, abstractmethod

from domain import ChaveCompra


class ChaveCompraRepositoryInterface(ABC):

    @abstractmethod
    def insert(self, chave_compra: ChaveCompra) -> ChaveCompra:
        raise NotImplementedError("Should implement method: insert")
