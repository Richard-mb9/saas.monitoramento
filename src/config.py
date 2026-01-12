from typing import Literal, cast

from decouple import config  # type: ignore
from dotenv import load_dotenv, find_dotenv

ENVIRONMENT: Literal["HML", "PRD", "local", "test"] = cast(
    Literal["HML", "PRD", "local", "test"], config("ENVIRONMENT", default="local")
)
dotenv = find_dotenv(f".env.{ENVIRONMENT.lower()}")
load_dotenv(dotenv)

# Database
USER_DB = config("USER_DB", default=None)
PASSWORD_DB = config("PASSWORD_DB", default=None)
HOST_DB = config("HOST_DB", default=None)
NAME_DB = config("NAME_DB", default=None)
PORT_DB = config("PORT_DB", default=None)
