from infra.integrations import Monitor
from infra.database_manager import DatabaseManagerConnection
from infra.repositories import RepositoryManager
from application.exceptions import BadRequestError


from .chat_monitor_use_case import ChatMonitorUseCase


class MonitorManagerUseCase:
    def __init__(self):
        self.monitors: dict[str, ChatMonitorUseCase] = {}
        self.db_manager = DatabaseManagerConnection()
        self._repository_manager = RepositoryManager(self.db_manager)

    def start(self, chat_id: str):
        if chat_id in self.monitors:
            raise BadRequestError("Chat já está sendo monitorado")

        chat_monitor = Monitor()
        monitor = ChatMonitorUseCase(
            chat_id=chat_id,
            monitor=chat_monitor,
            repository_manager=self._repository_manager,
        )
        monitor.start()
        self.monitors[chat_id] = monitor

    async def stop(self, chat_id: str):
        monitor = self.monitors.get(chat_id)
        self.db_manager.close_session()
        if not monitor:
            raise BadRequestError("Chat não está ativo")

        await monitor.stop()
        del self.monitors[chat_id]
