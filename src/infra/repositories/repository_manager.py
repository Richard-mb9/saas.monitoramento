from application.interfaces.repositories import RepositoryManagerInterface
from infra.database_manager import DatabaseManagerConnection
from .chave_compra_repository import ChaveCompraRepository
from .message_repository import MessageRepository


class RepositoryManager(RepositoryManagerInterface):

    def __init__(self, db_manager: DatabaseManagerConnection):
        self.db_manager = db_manager

    def message_repository(self) -> MessageRepository:
        return MessageRepository(self.db_manager)

    def chave_compra_repository(self) -> ChaveCompraRepository:
        return ChaveCompraRepository(self.db_manager)
