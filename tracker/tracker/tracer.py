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
            # Ensure we have a running event loop
            loop = asyncio.get_running_loop()
            # Create a Future to properly handle the async call
            future = loop.create_future()
            future.set_result(None)
            # Wait for put_trace to complete
            await client.put_trace(trace_id, ret.model_dump())  # type: ignore[func-returns-value]
            return ret

        return _async_capture_response

    @wraps(func)
    def _capture_response(*args: Any, **kwargs: Any) -> Any:
        trace_id = str(ULID())
        client = EvalTrackClient()
        ret: BaseModel = func(*args, **kwargs)
        # Create and set up event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Create a Future to properly handle the async call
            future = loop.create_future()
            future.set_result(None)
            # Run put_trace in the event loop
            loop.run_until_complete(client.put_trace(trace_id, ret.model_dump()))  # type: ignore[func-returns-value]
        finally:
            loop.close()
        return ret

    return _capture_response
