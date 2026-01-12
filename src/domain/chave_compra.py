from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChaveCompra:
    id_message: UUID
    id_uasg_identificacao: int
    id_modalidade: int
    numero: int
    ano: int
    numero_uasg: int
