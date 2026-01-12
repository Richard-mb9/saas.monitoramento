from http import HTTPStatus

from fastapi import APIRouter

from api.controllers import MonitorController
from application.use_cases.monitors import MonitorManagerUseCase

router = APIRouter()
monitor_manager = MonitorManagerUseCase()


@router.post("/start/{numeroCompra}", status_code=HTTPStatus.NO_CONTENT)
async def start(numeroCompra: str):
    MonitorController(monitor_manager).start(numero_compra=numeroCompra)


@router.post("/stop/{numeroCompra}", status_code=HTTPStatus.NO_CONTENT)
async def stop(numeroCompra: str):
    await MonitorController(monitor_manager).stop(numero_compra=numeroCompra)
