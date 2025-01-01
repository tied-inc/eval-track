from abc import ABC, abstractmethod
from typing import List, Optional

from core.session import with_session

from tracker.entity import Trace


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
    async def put_trace(self, trace: Trace) -> None:
        """Store a trace.

        Args:
            trace: The Trace object to store
        """
        pass

    @abstractmethod
    async def get_trace_by_id(self, trace_id: str) -> Optional[Trace]:
        """Retrieve a trace by ID.

        Args:
            trace_id: The unique identifier for the trace

        Returns:
            The Trace object if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_traces(self, limit: int = 100) -> List[Trace]:
        """Retrieve multiple traces.

        Args:
            limit: Maximum number of traces to retrieve (default: 100)

        Returns:
            List of Trace objects
        """
        pass

    @abstractmethod
    async def find_traces_with_artifacts(self) -> List[Trace]:
        """Find traces that have associated artifacts.

        Returns:
            List of Trace objects including their artifacts
        """
        pass


class PrismaStore(TraceStore):
    """Prisma implementation of the trace store interface."""

    async def put_trace(self, trace: Trace) -> None:
        """Store a trace in the database using Prisma.

        Args:
            trace: The Trace object to store
        """
        async with with_session() as db:
            trace_data = {
                "id": trace.id,
                "requestData": trace.request,
                "responseData": trace.response,
                "metadata": {"created_at": trace.created_at, "updated_at": trace.updated_at},
            }
            await db.trace.upsert(where={"id": trace.id}, create=trace_data, update=trace_data)

    async def get_trace_by_id(self, trace_id: str) -> Optional[Trace]:
        """Retrieve a trace from the database using Prisma.

        Args:
            trace_id: The unique identifier for the trace

        Returns:
            The Trace object if found, None otherwise
        """
        async with with_session() as db:
            trace = await db.trace.find_unique(where={"id": trace_id})
            if not trace:
                return None
            return Trace(
                id=trace.id,
                request=trace.requestData,
                response=trace.responseData,
                created_at=trace.metadata.get("created_at"),
                updated_at=trace.metadata.get("updated_at"),
            )

    async def get_traces(self, limit: int = 100) -> List[Trace]:
        """Retrieve multiple traces from the database using Prisma.

        Args:
            limit: Maximum number of traces to retrieve (default: 100)

        Returns:
            List of Trace objects
        """
        async with with_session() as db:
            traces = await db.trace.find_many(
                take=limit,
                order={"createdAt": "desc"},
            )
            return [
                Trace(
                    id=trace.id,
                    request=trace.requestData,
                    response=trace.responseData,
                    created_at=trace.metadata.get("created_at"),
                    updated_at=trace.metadata.get("updated_at"),
                )
                for trace in traces
            ]

    async def find_traces_with_artifacts(self) -> List[Trace]:
        """Find traces that have associated artifacts.

        Returns:
            List of Trace objects including their artifacts
        """
        async with with_session() as db:
            traces = await db.trace.find_many(
                include={"Artifacts": True},
                where={"Artifacts": {"some": {}}},
            )
            return [
                Trace(
                    id=trace.id,
                    request=trace.requestData,
                    response=trace.responseData,
                    created_at=trace.metadata.get("created_at"),
                    updated_at=trace.metadata.get("updated_at"),
                )
                for trace in traces
            ]
