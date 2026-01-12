from sqlalchemy import Table, Column, Integer, UUID

from domain import ChaveCompra

from .mapper_config import mapper_registry

chave_compra = Table(
    "chave_compra",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("id_message", UUID),
    Column("id_uasg_identificacao", Integer),
    Column("id_modalidade", Integer),
    Column("numero", Integer),
    Column("ano", Integer),
    Column("numero_uasg", Integer),
)

mapper_registry.map_imperatively(ChaveCompra, chave_compra)
