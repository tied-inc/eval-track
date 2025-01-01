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
            try:
                # Wait for put_trace to complete
                await client.put_trace(trace_id, ret.model_dump())  # type: ignore[func-returns-value]
            except Exception as e:
                logger.error(f"Error putting trace: {e}")
            return ret

        return _async_capture_response

    @wraps(func)
    def _capture_response(*args: Any, **kwargs: Any) -> Any:
        trace_id = str(ULID())
        client = EvalTrackClient()
        ret: BaseModel = func(*args, **kwargs)

        # Get the current event loop or create a new one
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            should_close = True
        else:
            should_close = False

        try:
            # Run put_trace in the event loop
            loop.run_until_complete(client.put_trace(trace_id, ret.model_dump()))  # type: ignore[func-returns-value]
        except Exception as e:
            logger.error(f"Error putting trace: {e}")
        finally:
            if should_close:
                loop.close()

        return ret

    return _capture_response
