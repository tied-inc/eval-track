"""Abstract base class for object storage implementations."""

from abc import ABC, abstractmethod
from typing import Optional


class StorageError(Exception):
    """Base exception class for storage-related errors."""

    pass


class AbstractObjectStorage(ABC):
    """Abstract base class for object storage implementations."""

    @abstractmethod
    def upload_log(self, key: str, data: bytes) -> None:
        """Upload log data to storage.

        Args:
            key: Unique identifier for the log data
            data: Raw bytes of log data to store

        Raises:
            StorageError: If the upload fails
        """
        pass

    @abstractmethod
    def get_log(self, key: str) -> Optional[bytes]:
        """Retrieve log data from storage.

        Args:
            key: Unique identifier for the log data to retrieve

        Returns:
            The log data as bytes if found, None if not found

        Raises:
            StorageError: If the retrieval fails for any reason
            other than the key not existing
        """
        pass
