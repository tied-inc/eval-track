import asyncio
import logging
from functools import wraps
from typing import Any, Callable

import httpx
from fastapi import BackgroundTasks
from pydantic import BaseModel
from ulid import ULID

from tracker.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()


def put_trace(trace_id: str, data: dict) -> None:
    try:
        with httpx.Client() as client:
            ret = client.put(f"{settings.eval_tracker_base_url}/traces/{trace_id}", data=data)
            if ret.status_code != httpx.codes.OK:
                logger.error(f"receive not ok status code: {ret.status_code}")
            logger.info("put trace succeeded")
    except Exception:
        logger.error("receive unexpected error")


def capture_response(func: Callable) -> Callable:
    """Decorator that captures the response from a function or coroutine.

    This decorator wraps both synchronous and asynchronous functions to capture their
    return values. It preserves the original function's signature and attributes
    through the use of @wraps.

    Args:
        func (Callable): The function to be decorated. Can be either a regular function
            or a coroutine function.

    Returns:
        Callable: A wrapped function that captures the response while maintaining the
        original function's behavior.
    """
    bt = BackgroundTasks()
    trace_id = str(ULID())
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def _async_capture_response(*args: Any, **kwargs: Any) -> Any:
            ret: BaseModel = await func(*args, **kwargs)
            bt.add_task(put_trace, trace_id, ret.model_dump())
            return ret

        return _async_capture_response

    @wraps(func)
    def _capture_response(*args: Any, **kwargs: Any) -> Any:
        ret: BaseModel = func(*args, **kwargs)
        bt.add_task(put_trace, trace_id, ret.model_dump())
        return ret

    return _capture_response
