from typing import Optional, Any, Dict
from uuid import UUID
from asyncio import sleep, CancelledError, Event, Task, create_task, gather

from application.interfaces import MonitorInterface
from application.interfaces.repositories import RepositoryManagerInterface

from domain import ChaveCompra, Message


class ChatMonitorUseCase:
    def __init__(
        self,
        chat_id: str,
        monitor: MonitorInterface,
        repository_manager: RepositoryManagerInterface,
    ):
        self.chat_id = chat_id
        self._stop_event = Event()
        self._task: Optional[Task[Any]] = None
        self._monitor = monitor
        self._message_repository = repository_manager.message_repository()
        self._chave_compra_repository = repository_manager.chave_compra_repository()

    async def run(self):
        print(f"Monitor iniciado: {self.chat_id}")
        try:
            while not self._stop_event.is_set():
                await self.check_chat()
                await sleep(30)
        except CancelledError:
            pass
        finally:
            print(f"Monitor finalizado: {self.chat_id}")

    async def check_chat(self):
        try:
            print(f"Verificando chat {self.chat_id}")
            messages = await self._monitor.get_messages(self.chat_id)
            for msg in messages:
                message_in_db = self._message_repository.find_by_id(
                    UUID(msg.get("chaveMensagemNaOrigem"))
                )
                if message_in_db is None:
                    self.__save_message(msg)

        except Exception as error:
            print("Houve um erro ao obter as mensagesns", error.args)

    def start(self):
        if self._task and not self._task.done():
            raise RuntimeError("Monitor já está ativo")

        self._stop_event.clear()
        self._task = create_task(self.run())

    async def stop(self):
        self._stop_event.set()
        if self._task:
            self._task.cancel()
            await gather(self._task, return_exceptions=True)

    def __save_message(self, msg: Dict[str, Any]):
        id_message = UUID(msg.get("chaveMensagemNaOrigem"))
        chave_compra = self.__build_chave_compra_entity(
            id_message=id_message, chave_compra=msg["chaveCompra"]
        )
        message = self.__build_message_entity(id_message=id_message, message=msg)

        self._message_repository.insert(message)
        self._chave_compra_repository.insert(chave_compra)

    def __build_chave_compra_entity(
        self, id_message: UUID, chave_compra: Dict[str, int]
    ) -> ChaveCompra:
        return ChaveCompra(
            id_message=id_message,
            id_uasg_identificacao=chave_compra["idUasgIdentificacao"],
            id_modalidade=chave_compra["idModalidade"],
            numero=chave_compra["numero"],
            ano=chave_compra["numeroUasg"],
            numero_uasg=chave_compra["numeroUasg"],
        )

    def __build_message_entity(
        self, id_message: UUID, message: Dict[str, Any]
    ) -> Message:
        return Message(
            id=id_message,
            identificador_item=message["identificadorItem"],
            tipo_rementente=Message.obter_tipo_remetente(message["tipoRemetente"]),
            texto=message["texto"],
            categoria=message["categoria"],
            data_hora=message["dataHora"],
            cnpj_destinatario=message.get("identificadorDestinatario"),
            cnpj_remetente=message.get("identificadorRemetente"),
        )
