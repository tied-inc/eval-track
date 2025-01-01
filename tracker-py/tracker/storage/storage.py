"""Storage providers for eval-track logs."""

from abc import ABC, abstractmethod
from typing import Optional


class StorageError(Exception):
    """Base exception class for storage-related errors."""

    pass


class AbstractObjectStorage(ABC):
    """Abstract base class for cloud storage providers."""

    @abstractmethod
    def upload_log(self, key: str, data: bytes) -> None:
        """Upload log data to the storage provider.

        Args:
            key: Unique identifier for the log data
            data: Raw bytes of log data to store

        Raises:
            StorageError: If the upload fails for any reason
        """
        pass

    @abstractmethod
    def get_log(self, key: str) -> Optional[bytes]:
        """Retrieve log data from the storage provider.

        Args:
            key: Unique identifier for the log data to retrieve

        Returns:
            The log data as bytes if found, None if not found

        Raises:
            StorageError: If the retrieval fails for any reason
        """
        pass
