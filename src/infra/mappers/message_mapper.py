from sqlalchemy import Table, Column, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from domain import Message

from .mapper_config import mapper_registry
from .chave_compra_mapper import chave_compra

messages = Table(
    "messages",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("tipo_remetente", String),
    Column("identificador_item", Integer),
    Column("texto", Text),
    Column("categoria", String),
    Column("data_hora", DateTime),
    Column("created_at", DateTime, nullable=False),
    Column("cnpj_rementente", String, nullable=True),
    Column("cnpj_destinatario", String, nullable=True),
)

mapper_registry.map_imperatively(
    Message,
    messages,
    properties={
        "chave_compra": relationship(
            "ChaveCompra",
            primaryjoin=messages.c.id == chave_compra.c.id_message,
            foreign_keys=[chave_compra.c.id_message],
            uselist=False,
            backref="message",
        )
    },
)
