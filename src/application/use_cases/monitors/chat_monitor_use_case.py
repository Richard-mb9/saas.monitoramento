from typing import Optional, Any
from asyncio import sleep, CancelledError, Event, Task, create_task, gather

from application.interfaces import MonitorInterface
from application.interfaces.repositories import RepositoryManagerInterface


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
                print(msg["texto"])
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
