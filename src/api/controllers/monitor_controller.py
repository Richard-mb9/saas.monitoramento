from application.use_cases.monitors import MonitorManagerUseCase


class MonitorController:
    def __init__(self, monitor_manager: MonitorManagerUseCase) -> None:
        self.monitor_manager = monitor_manager

    def start(self, numero_compra: str) -> None:
        self.monitor_manager.start(numero_compra)

    async def stop(self, numero_compra: str) -> None:
        await self.monitor_manager.stop(numero_compra)
