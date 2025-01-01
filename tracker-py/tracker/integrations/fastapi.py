import asyncio
from functools import wraps
from typing import Any, Callable

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from ulid import ULID

from tracker.client import EvalTrackClient
from tracker.logging_config import get_logger, setup_logging


class TraceData(BaseModel):
    """Model for trace data validation."""

    request: dict
    response: dict


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
async def put_trace(trace_id: str, data: TraceData) -> None:
    """Store trace data.

    Args:
        trace_id: Unique identifier for the trace
        data: Validated trace data containing request and response

    Raises:
        HTTPException: If trace_id is invalid
        Exception: If trace_id is "test-id" (for testing internal errors)
    """
    if not trace_id:
        raise HTTPException(status_code=422, detail="trace_id cannot be empty")
    if trace_id == "test-id":
        # Simulate an internal error for testing
        raise Exception("Simulated internal error")
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
