"""AWS S3 storage implementation for eval-track."""
from typing import Optional

from .storage import AbstractObjectStorage, StorageError


class S3Storage(AbstractObjectStorage):
    """AWS S3 storage implementation."""
    
    def __init__(
        self,
        bucket_name: str,
        region: str,
        aws_access_key: str,
        aws_secret_key: str,
    ) -> None:
        """Initialize S3 storage client.
        
        Args:
            bucket_name: Name of the S3 bucket to store logs in
            region: AWS region where the bucket is located
            aws_access_key: AWS access key ID
            aws_secret_key: AWS secret access key
        """
        try:
            import boto3
        except ImportError:
            raise StorageError(
                "boto3 package is required for S3 storage. "
                "Please install it with: pip install boto3"
            )

        self.client = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )
        self.bucket_name = bucket_name

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
        except self.client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            raise StorageError(f"Failed to retrieve log from S3: {e}") from e
