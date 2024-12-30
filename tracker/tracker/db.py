import warnings
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class AbstractKeyValueStore(ABC):
    """Abstract base class for key-value storage implementations.

    DEPRECATED: This interface is maintained only for backward compatibility.
    New code should use either:

    1. PrismaStore (recommended for existing key-value store usage):
        ```python
        from tracker.prisma_store import PrismaStore
        store = PrismaStore()
        await store.put_item(key, value)
        ```

    2. Direct Prisma client (recommended for new features):
        ```python
        from core.core.session import with_session
        async with with_session() as db:
            await db.trace.create(...)
        ```

    The direct Prisma client approach is preferred for new features as it provides
    access to the full Prisma API including relations and complex queries.
    """

    @abstractmethod
    async def put_item(self, key: str, value: dict) -> None:
        """Store an item in the key-value store.

        Args:
            key: The unique identifier for the item
            value: The data to store
        """
        pass


class DynamoDB(AbstractKeyValueStore):
    """Legacy DynamoDB implementation.

    Deprecated: Use PrismaStore or direct Prisma client instead.
    This class is maintained only for backward compatibility during migration.
    """

    def __init__(self) -> None:
        warnings.warn(
            "DynamoDB storage is deprecated and will be removed in a future version. "
            "Use PrismaStore for direct replacement or Prisma client for new features. "
            "See class docstring for migration examples.",
            DeprecationWarning,
            stacklevel=2,
        )
        ...

    async def put_item(self, key: str, value: dict) -> None:
        warnings.warn(
            "DynamoDB storage is deprecated and will be removed in a future version. "
            "Use PrismaStore for direct replacement or Prisma client for new features. "
            "See class docstring for migration examples.",
            DeprecationWarning,
            stacklevel=2,
        )
        ...


class Redis(AbstractKeyValueStore):
    """Legacy Redis implementation.

    Deprecated: Use PrismaStore or direct Prisma client instead.
    This class is maintained only for backward compatibility during migration.
    """

    def __init__(self) -> None:
        warnings.warn(
            "Redis storage is deprecated and will be removed in a future version. "
            "Use PrismaStore for direct replacement or Prisma client for new features. "
            "See class docstring for migration examples.",
            DeprecationWarning,
            stacklevel=2,
        )
        ...


class TraceStore(ABC):
    """Abstract base class for trace storage implementations.

    This class defines the interface for storing and retrieving traces.
    It is designed specifically for trace operations and should be used
    instead of the deprecated AbstractKeyValueStore for all new code.

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

    async def put_item(self, key: str, value: dict) -> None:
        warnings.warn(
            "Redis storage is deprecated and will be removed in a future version. "
            "Use PrismaStore for direct replacement or Prisma client for new features. "
            "See class docstring for migration examples.",
            DeprecationWarning,
            stacklevel=2,
        )
        ...
