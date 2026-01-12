from typing import Dict, Any, List
from abc import ABC, abstractmethod


class MonitorInterface(ABC):

    @abstractmethod
    async def get_messages(self, numero_compra: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("Should implement method: get_messages")

    async def close(self) -> None:
        raise NotImplementedError("Should implement method: close")
