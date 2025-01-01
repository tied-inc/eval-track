from fastapi import APIRouter

from tracker.logging_config import get_logger, setup_logging
import asyncio
import logging
from functools import wraps
from typing import Any, Callable

from fastapi import BackgroundTasks
from pydantic import BaseModel
from ulid import ULID

from tracker.client import EvalTrackClient


# Ensure logging is configured
setup_logging()

router = APIRouter(prefix="/eval-track")
logger = get_logger(__name__)


@router.get("/health")
def get_health() -> str:
    logger.info("Health check endpoint called")
    return "OK"


@router.get("/traces")
async def get_traces() -> dict:
    logger.info("Logs retrieval endpoint called")
    return {"message": "Logs endpoint"}


@router.put("/traces/{trace_id}", status_code=204)
async def put_trace(trace_id: str, data: dict) -> None:
    logger.info(f"Received logs with traceId: {trace_id}")


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
            bt.add_task(client.put_trace, trace_id, ret.model_dump())
            return ret

        return _async_capture_response

    @wraps(func)
    def _capture_response(*args: Any, **kwargs: Any) -> Any:
        ret: BaseModel = func(*args, **kwargs)
        bt.add_task(client.put_trace, trace_id, ret.model_dump())
        return ret

    return _capture_response
