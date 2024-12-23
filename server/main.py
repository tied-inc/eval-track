from fastapi import FastAPI, APIRouter
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
router = APIRouter()
logger = logging.getLogger(__name__)


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


if __name__ == "__main__":
    app = FastAPI()
    app.include_router()
