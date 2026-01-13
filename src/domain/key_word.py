from uuid import UUID
from datetime import datetime
from typing import Optional


class KeyWord:
    def __init__(
        self,
        id: UUID,
        numero_compra: str,
        palavra: str,
        ativo: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.numero_compra = numero_compra
        self.palavra = palavra
        self.ativo = ativo
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at
