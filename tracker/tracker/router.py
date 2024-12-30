import logging

from core.core.session import with_session
from fastapi import APIRouter

logging.getLogger(__name__).addHandler(logging.NullHandler())
router = APIRouter(prefix="/eval-track")
logger = logging.getLogger(__name__)


@router.get("/health")
def get_health() -> str:
    logger.info("Health check endpoint called")
    return "OK"


@router.get("/traces")
async def get_traces() -> dict:
    logger.info("Logs retrieval endpoint called")
    async with with_session() as db:
        traces = await db.trace.find_many(include={"Artifacts": True})
        return {"traces": [trace.dict() for trace in traces]}


@router.put("/traces/{trace_id}", status_code=204)
async def put_trace(trace_id: str, data: dict) -> None:
    logger.info(f"Received logs with traceId: {trace_id}")
    async with with_session() as db:
        await db.trace.upsert(
            where={"id": trace_id},
            create={
                "id": trace_id,
                "requestData": data.get("request"),
                "responseData": data.get("response"),
                "metadata": {"created_at": data.get("created_at"), "updated_at": data.get("updated_at")},
            },
            update={
                "requestData": data.get("request"),
                "responseData": data.get("response"),
                "metadata": {"updated_at": data.get("updated_at")},
            },
        )
