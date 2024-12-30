"""Storage package for eval-track."""

from .s3 import S3Storage
from .storage import AbstractObjectStorage, StorageError

__all__ = ["AbstractObjectStorage", "StorageError", "S3Storage"]
