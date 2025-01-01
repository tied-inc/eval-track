from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from tracker.logging_config import get_logger

router = APIRouter(prefix="/eval-track")
logger = get_logger(__name__)


@router.get("/health")
def get_health() -> str:
    logger.info("Health check endpoint called")
    return "OK"


@router.get("/test-internal-error")
def test_internal_error() -> None:
    """Endpoint that always raises an exception for testing error handling."""
    raise Exception("Test internal server error")


@router.get("/traces")
async def get_traces() -> list[dict]:
    logger.info("Logs retrieval endpoint called")

    return []


class TraceData(BaseModel):
    request: dict
    response: dict


@router.put("/traces/{trace_id}", status_code=204)
async def put_trace(trace_id: str, data: TraceData) -> None:
    """Store trace data for the given trace ID.

    Args:
        trace_id: Unique identifier for the trace
        data: Request and response data for the trace

    Raises:
        HTTPException: If validation fails
    """
    if not trace_id:
        raise HTTPException(status_code=422, detail="Trace ID cannot be empty")

    try:
        # Validate request data
        if not data.request or not data.response:
            raise HTTPException(status_code=422, detail="Both request and response data are required")

        logger.info(f"Received logs with traceId: {trace_id}")
    except Exception as e:
        logger.error(f"Error processing trace: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
