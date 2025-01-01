import logging

from core.session import with_session

from tracker.prisma_store import PrismaStore

logger = logging.getLogger(__name__)


class EvalTrackClient:
    def __init__(self) -> None:
        self.store = PrismaStore()

    async def get_traces(self) -> dict:
        logger.info("Getting traces from database")
        try:
            async with with_session() as db:
                traces = await db.trace.find_many(include={"Artifacts": True})
                return {"traces": [trace.dict() for trace in traces]}
        except Exception:
            logger.error("Failed to get traces from database")
            return {}

    async def put_trace(self, trace_id: str, data: dict) -> None:
        logger.info(f"Storing trace with ID: {trace_id}")
        try:
            await self.store.put_trace(trace_id, data)
            logger.info("Successfully stored trace")
        except Exception:
            logger.error("Failed to store trace in database")
