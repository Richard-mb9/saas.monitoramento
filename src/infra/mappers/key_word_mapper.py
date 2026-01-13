from sqlalchemy import Table, Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

from domain import KeyWord

from .mapper_config import mapper_registry

key_word = Table(
    "key_words",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("numero_compra", String, nullable=False, index=True),
    Column("palavra", String, nullable=False),
    Column("ativo", Boolean, default=True),
    Column("created_at", DateTime, nullable=True),
    Column("updated_at", DateTime, nullable=True),
)

mapper_registry.map_imperatively(KeyWord, key_word)
