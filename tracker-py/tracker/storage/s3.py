"""AWS S3 storage implementation for eval-track."""

import os
from typing import Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, EndpointConnectionError

from tracker.settings import settings

from .storage import AbstractObjectStorage, StorageError


class S3Storage(AbstractObjectStorage):
    """AWS S3 storage implementation."""

    def __init__(self) -> None:
        """Initialize S3 storage client using settings configuration.

        Raises:
            StorageError: If boto3 package is not available or if settings are invalid
        """
        try:
            import boto3
            from botocore.config import Config
            from botocore.exceptions import ClientError, EndpointConnectionError

            self.bucket_name = settings.s3_bucket
            config = Config(signature_version="s3v4")

            # Build client kwargs
            client_kwargs = {
                "service_name": "s3",
                "region_name": settings.s3_region,
                "aws_access_key_id": str(settings.s3_access_key.get_secret_value()),
                "aws_secret_access_key": str(settings.s3_secret_key.get_secret_value()),
                "config": config,
            }

            # Add endpoint_url if specified in environment
            endpoint_url = os.getenv("AWS_ENDPOINT_URL")
            if endpoint_url:
                client_kwargs["endpoint_url"] = endpoint_url

            try:
                self.client = boto3.client(**client_kwargs)
                # Test if bucket exists and is accessible
                self.client.head_bucket(Bucket=self.bucket_name)
            except (ClientError, EndpointConnectionError, ValueError) as e:
                raise StorageError(f"Failed to initialize S3 storage: {str(e)}")
        except ImportError:
            raise StorageError(
                "boto3 package is required for S3 storage. " "Please install it with: pip install boto3"
            )

    def upload_log(self, key: str, data: bytes) -> None:
        """Upload log data to S3.

        Args:
            key: Unique identifier for the log data
            data: Raw bytes of log data to store

        Raises:
            StorageError: If the upload fails
        """
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=data,
            )
        except Exception as e:
            raise StorageError(f"Failed to upload log to S3: {e}") from e

    def get_log(self, key: str) -> Optional[bytes]:
        """Retrieve log data from S3.

        Args:
            key: Unique identifier for the log data to retrieve

        Returns:
            The log data as bytes if found, None if not found

        Raises:
            StorageError: If the retrieval fails for any reason
            other than the key not existing
        """
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=key,
            )
            return response["Body"].read()
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            raise StorageError(f"Failed to retrieve log from S3: {e}") from e
        except Exception as e:
            raise StorageError(f"Failed to retrieve log from S3: {e}") from e
