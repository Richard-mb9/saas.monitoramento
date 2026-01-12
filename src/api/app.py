# pylint: disable=W0613
from http import HTTPStatus
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from infra.mappers import import_mappers
from application.exceptions.application_exceptions import APIError


# from config import ENVIRONMENT
from .routers import create_routes

URL_PREFIX = "/chat-monitor-service"
API_DOC = f"{URL_PREFIX}/doc/api"
API_DOC_REDOC = f"{URL_PREFIX}/doc/redoc"
API_DOC_JSON = f"{URL_PREFIX}/doc/api.json"
API_VERSION = "V1.0.0"


def create_app():
    import_mappers()
    api = FastAPI(
        # root_path=f"/{ENVIRONMENT}",
        title="Chat Monitor Service",
        description="Api for manage Chat Monitors",
        openapi_url=API_DOC_JSON,
        redoc_url=API_DOC_REDOC,
        docs_url=API_DOC,
        version=API_VERSION,
    )

    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @api.exception_handler(APIError)
    def http_exception_handler(request: Request, error: APIError):  # type: ignore
        return JSONResponse(
            content={"detail": error.message}, status_code=error.status_code
        )

    @api.exception_handler(RequestValidationError)
    async def validation_exception_handler(  # type: ignore
        request: Request, exc: RequestValidationError
    ):
        errors = exc.errors()
        response = {}
        for error in errors:
            key = error["loc"][1]
            response[key] = error["msg"]
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"detail": response},
        )

    return create_routes(api, URL_PREFIX)


app = create_app()
