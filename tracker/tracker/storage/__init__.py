"""Storage package for eval-track."""
from .storage import AbstractObjectStorage, StorageError
from .s3 import S3Storage

__all__ = ["AbstractObjectStorage", "StorageError", "S3Storage"]
