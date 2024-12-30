import warnings
from abc import ABC, abstractmethod


class AbstractKeyValueStore(ABC):
    """Abstract base class for key-value storage implementations.

    This interface is maintained for backward compatibility, but new code should
    use the Prisma client directly through the with_session context manager.

    Example:
        ```python
        from core.core.session import with_session

        async with with_session() as db:
            await db.trace.create(...)
        ```
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
            "DynamoDB storage is deprecated. Use PrismaStore or Prisma client directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        ...

    async def put_item(self, key: str, value: dict) -> None:
        warnings.warn(
            "DynamoDB storage is deprecated. Use PrismaStore or Prisma client directly.",
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
            "Redis storage is deprecated. Use PrismaStore or Prisma client directly.", DeprecationWarning, stacklevel=2
        )
        ...

    async def put_item(self, key: str, value: dict) -> None:
        warnings.warn(
            "Redis storage is deprecated. Use PrismaStore or Prisma client directly.", DeprecationWarning, stacklevel=2
        )
        ...
