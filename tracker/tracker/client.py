import logging
from typing import Dict, List

from tracker.entity import Trace
from tracker.prisma_store import PrismaStore

logger = logging.getLogger(__name__)


class EvalTrackClient:
    def __init__(self, store: PrismaStore) -> None:
        self.store = store

    async def get_traces(self) -> Dict[str, List[Dict]]:
        logger.info("Getting traces from database")
        try:
            traces = await self.store.get_traces()
            return {"traces": [
                {
                    "id": trace.id,
                    "request": trace.request,
                    "response": trace.response,
                    "created_at": trace.created_at,
                    "updated_at": trace.updated_at,
                }
                for trace in traces
            ]}
        except Exception:
            logger.error("Failed to get traces from database")
            return {"traces": []}

    async def put_trace(self, trace_id: str, data: dict) -> None:
        logger.info(f"Storing trace with ID: {trace_id}")
        try:
            trace = Trace(
                id=trace_id,
                request=data.get("request", {}),
                response=data.get("response", {}),
                created_at=data.get("created_at", ""),
                updated_at=data.get("updated_at", ""),
            )
            await self.store.put_trace(trace)
            logger.info("Successfully stored trace")
        except Exception:
            logger.error("Failed to store trace in database")
