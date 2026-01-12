from uuid import UUID
from typing import Optional
from application.interfaces.repositories import MessageRepositoryInterface
from infra.database_manager import DatabaseManagerConnection

from domain import Message


class MessageRepository(MessageRepositoryInterface):

    def __init__(self, db_manager: DatabaseManagerConnection):
        self.session = db_manager.session

    def insert(self, message: Message) -> Message:
        self.session.add(message)
        self.session.commit()
        return message

    def find_by_id(self, message_id: UUID) -> Optional[Message]:
        return self.session.query(Message).filter_by(id=message_id).first()
