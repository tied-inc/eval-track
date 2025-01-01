from fastapi import APIRouter

from tracker.logging_config import get_logger, setup_logging

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
