from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from core.core.session import with_session


class TraceStore(ABC):
    """Abstract base class for trace storage implementations.

    This class defines the interface for storing and retrieving traces.
    It is designed specifically for trace operations and provides a clean
    abstraction for trace-specific storage operations.

    Example:
        ```python
        class MyTraceStore(TraceStore):
            async def put_trace(self, trace_id: str, data: dict) -> None:
                # Implementation
                pass
        ```
    """

    @abstractmethod
    async def put_trace(self, trace_id: str, data: dict) -> None:
        """Store a trace with the given ID.

        Args:
            trace_id: The unique identifier for the trace
            data: The trace data containing request and response information
        """
        pass

    @abstractmethod
    async def get_trace(self, trace_id: str) -> Optional[Dict]:
        """Retrieve a trace by ID.

        Args:
            trace_id: The unique identifier for the trace

        Returns:
            The trace data if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_traces(self, limit: int = 100) -> List[Dict]:
        """Retrieve multiple traces.

        Args:
            limit: Maximum number of traces to retrieve (default: 100)

        Returns:
            List of trace data dictionaries
        """
        pass

    @abstractmethod
    async def find_traces_with_artifacts(self) -> List[Dict]:
        """Find traces that have associated artifacts.

        Returns:
            List of trace data dictionaries including their artifacts
        """
        pass


class PrismaStore(TraceStore):
    """Prisma implementation of the trace store interface."""

    async def put_trace(self, trace_id: str, data: dict) -> None:
        """Store a trace in the database using Prisma.

        Args:
            trace_id: The unique identifier for the trace
            data: The trace data containing request and response information
        """
        async with with_session() as db:
            trace_data = {
                "id": trace_id,
                "requestData": data.get("request"),
                "responseData": data.get("response"),
                "metadata": {"created_at": data.get("created_at"), "updated_at": data.get("updated_at")},
            }
            await db.trace.upsert(where={"id": trace_id}, create=trace_data, update=trace_data)

    async def get_trace(self, trace_id: str) -> Optional[Dict]:
        """Retrieve a trace from the database using Prisma.

        Args:
            trace_id: The unique identifier for the trace

        Returns:
            The trace data if found, None otherwise
        """
        async with with_session() as db:
            trace = await db.trace.find_unique(where={"id": trace_id})
            if not trace:
                return None
            return {
                "id": trace.id,
                "request": trace.requestData,
                "response": trace.responseData,
                **(trace.metadata or {}),
            }

    async def get_traces(self, limit: int = 100) -> List[Dict]:
        """Retrieve multiple traces from the database using Prisma.

        Args:
            limit: Maximum number of traces to retrieve (default: 100)

        Returns:
            List of trace data dictionaries
        """
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

    async def find_traces_with_artifacts(self) -> List[Dict]:
        """Find traces that have associated artifacts.

        Returns:
            List of trace data dictionaries including their artifacts
        """
        async with with_session() as db:
            traces = await db.trace.find_many(
                include={"Artifacts": True},
                where={"Artifacts": {"some": {}}},
            )
            return [
                {
                    "id": trace.id,
                    "request": trace.requestData,
                    "response": trace.responseData,
                    **(trace.metadata or {}),
                    "artifacts": [artifact.dict() for artifact in trace.Artifacts],
                }
                for trace in traces
            ]
