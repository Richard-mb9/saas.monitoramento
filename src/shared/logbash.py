from typing import Any
import contextvars
import logging

chat_id_ctx = contextvars.ContextVar("chat_id", default="")
old_factory = logging.getLogRecordFactory()


def record_factory(*args: Any, **kwargs: Any):
    record = old_factory(*args, **kwargs)
    record.chat_id = get_chat_id()
    return record


def set_chat_id(value: str):
    chat_id_ctx.set(value)


def get_chat_id():
    return chat_id_ctx.get()


logging.setLogRecordFactory(record_factory)
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(chat_id)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
