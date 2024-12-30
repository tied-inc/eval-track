import warnings
from abc import ABC, abstractmethod


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
            stacklevel=2
        )
        ...

    async def put_item(self, key: str, value: dict) -> None:
        warnings.warn(
            "Redis storage is deprecated and will be removed in a future version. "
            "Use PrismaStore for direct replacement or Prisma client for new features. "
            "See class docstring for migration examples.",
            DeprecationWarning,
            stacklevel=2
        )
        ...
