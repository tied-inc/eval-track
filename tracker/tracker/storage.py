"""Storage providers for eval-track logs.

This module provides abstract and concrete implementations for storing logs
in various cloud storage providers like S3, GCS, and R2.
"""
from abc import ABC, abstractmethod
from typing import Optional


class AbstractObjectStorage(ABC):
    """Abstract base class for cloud storage providers.
    
    This class defines the interface that all storage providers must implement
    to be used with eval-track for storing logs.
    """
    
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


class StorageError(Exception):
    """Base exception class for storage-related errors."""
    pass
