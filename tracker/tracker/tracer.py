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
    bt = BackgroundTasks()
    trace_id = str(ULID())
    client = EvalTrackClient()

    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def _async_capture_response(*args: Any, **kwargs: Any) -> Any:
            ret: BaseModel = await func(*args, **kwargs)
            # Add async task to background tasks
            async def _store_trace():
                await client.put_trace(trace_id, ret.model_dump())
            bt.add_task(_store_trace)
            return ret

        return _async_capture_response

    @wraps(func)
    def _capture_response(*args: Any, **kwargs: Any) -> Any:
        ret: BaseModel = func(*args, **kwargs)
        # Create async task for sync functions
        async def _store_trace():
            await client.put_trace(trace_id, ret.model_dump())
        bt.add_task(_store_trace)
        return ret

    return _capture_response
