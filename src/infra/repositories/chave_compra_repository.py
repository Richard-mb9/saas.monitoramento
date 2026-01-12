from application.interfaces.repositories import ChaveCompraRepositoryInterface
from domain.chave_compra import ChaveCompra
from infra.database_manager import DatabaseManagerConnection


class ChaveCompraRepository(ChaveCompraRepositoryInterface):
    def __init__(self, db_manager: DatabaseManagerConnection):
        self.session = db_manager.session

    def insert(self, chave_compra: ChaveCompra) -> ChaveCompra:
        self.session.add(chave_compra)
        self.session.commit()
        return chave_compra
