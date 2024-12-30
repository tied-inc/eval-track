from typing import Dict, List, Optional

from core.core.session import with_session

from tracker.db import AbstractKeyValueStore


class PrismaStore(AbstractKeyValueStore):
    """Prisma implementation of the key-value store interface."""

    async def put_item(self, key: str, value: dict) -> None:
        """Store a trace item in the database using Prisma."""
        async with with_session() as db:
            # Convert the value dict to match our Prisma schema
            trace_data = {
                "id": key,
                "requestData": value.get("request"),
                "responseData": value.get("response"),
                "metadata": {"created_at": value.get("created_at"), "updated_at": value.get("updated_at")},
            }

            # Create or update the trace
            await db.trace.upsert(where={"id": key}, create=trace_data, update=trace_data)

    async def get_item(self, key: str) -> Optional[Dict]:
        """Retrieve a trace item from the database using Prisma."""
        async with with_session() as db:
            trace = await db.trace.find_unique(where={"id": key})
            if not trace:
                return None
            return {
                "id": trace.id,
                "request": trace.requestData,
                "response": trace.responseData,
                **(trace.metadata or {}),
            }

    async def get_items(self, limit: int = 100) -> List[Dict]:
        """Retrieve multiple trace items from the database using Prisma."""
        async with with_session() as db:
            traces = await db.trace.find_many(
                take=limit,
                order={"createdAt": "desc"},
            )
            return [
                {
                    "id": trace.id,
                    "request": trace.requestData,
                    "response": trace.responseData,
                    **(trace.metadata or {}),
                }
                for trace in traces
            ]
