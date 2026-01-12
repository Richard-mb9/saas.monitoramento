from typing import Literal, Dict, Optional, TYPE_CHECKING
from uuid import UUID
from datetime import datetime

if TYPE_CHECKING:
    from .chave_compra import ChaveCompra

TIPO_REMETENTE = Literal["SISTEMA", "", "USUARIO_FORNECEDOR", "USUARIO_GOVERNO"]


class Message:
    chave_compra: "ChaveCompra"

    def __init__(
        self,
        id: UUID,  # chaveMensagemNaOrigem
        tipo_rementente: TIPO_REMETENTE,
        identificador_item: int,
        texto: str,
        categoria: str,
        data_hora: datetime,
        cnpj_remetente: Optional[str] = None,  # identificadorRemetente
        cnpj_destinatario: Optional[str] = None,  # identificadorDestinatario
    ) -> None:
        self.id = id
        self.tipo_remetente = tipo_rementente
        self.identificador_item = identificador_item
        self.texto = texto
        self.categoria = categoria
        self.data_hora = data_hora
        self.cnpj_rementente = cnpj_remetente
        self.cnpj_destinatario = cnpj_destinatario

    def obter_tipo_remetente(self, id_tipo_rementente: int) -> TIPO_REMETENTE:
        users: Dict[str, TIPO_REMETENTE] = {
            "0": "SISTEMA",
            "1": "USUARIO_FORNECEDOR",
            "3": "USUARIO_GOVERNO",
        }

        if str(id_tipo_rementente) not in users:
            raise ValueError("id_tipo_rementente invalido")

        return users[str(id_tipo_rementente)]
