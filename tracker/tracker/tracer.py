import asyncio
import logging
from functools import wraps
from typing import Any, Callable

from fastapi import BackgroundTasks
from pydantic import BaseModel
from ulid import ULID

from tracker.client import EvalTrackClient

logger = logging.getLogger(__name__)


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
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def _async_capture_response(*args: Any, **kwargs: Any) -> Any:
            trace_id = str(ULID())
            client = EvalTrackClient()
            ret: BaseModel = await func(*args, **kwargs)
            # Call put_trace as a statement since it returns None
            await client.put_trace(trace_id, ret.model_dump())
            return ret

        return _async_capture_response

    @wraps(func)
    def _capture_response(*args: Any, **kwargs: Any) -> Any:
        trace_id = str(ULID())
        client = EvalTrackClient()
        ret: BaseModel = func(*args, **kwargs)
        # Call put_trace as a statement since it returns None
        asyncio.run(client.put_trace(trace_id, ret.model_dump()))
        return ret

    return _capture_response
