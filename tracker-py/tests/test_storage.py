"""Test suite for storage backends."""

from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from tracker.settings import settings
from tracker.storage.s3 import S3Storage, StorageError


@pytest.fixture
def mock_boto3() -> Generator[MagicMock, Any, None]:
    """Mock boto3 client for testing."""
    with patch("boto3.client") as mock_client:
        yield mock_client


@pytest.fixture
def s3_storage(mock_boto3: MagicMock) -> S3Storage:
    """Create S3Storage instance with mocked boto3."""
    return S3Storage()


def test_s3_init_missing_boto3() -> None:
    """Test S3Storage initialization fails when boto3 is not available."""
    with patch.dict("sys.modules", {"boto3": None}):
        with pytest.raises(StorageError, match="boto3 package is required"):
            S3Storage()


def test_s3_upload_log_success(s3_storage: S3Storage, mock_boto3: MagicMock) -> None:
    """Test successful log upload to S3."""
    test_key = "test-key"
    test_data = b"test data"

    s3_storage.upload_log(test_key, test_data)

    # Verify put_object was called with correct arguments
    mock_boto3.return_value.put_object.assert_called_once_with(
        Bucket=settings.s3_bucket,
        Key=test_key,
        Body=test_data,
    )


def test_s3_upload_log_failure(s3_storage: S3Storage, mock_boto3: MagicMock) -> None:
    """Test upload_log handles S3 errors properly."""
    mock_boto3.return_value.put_object.side_effect = Exception("S3 error")

    with pytest.raises(StorageError, match="Failed to upload log to S3"):
        s3_storage.upload_log("test-key", b"test data")


def test_s3_get_log_success(s3_storage: S3Storage, mock_boto3: MagicMock) -> None:
    """Test successful log retrieval from S3."""
    test_key = "test-key"
    test_data = b"test data"

    # Mock successful response
    mock_response = {"Body": MagicMock()}
    mock_response["Body"].read.return_value = test_data
    mock_boto3.return_value.get_object.return_value = mock_response

    result = s3_storage.get_log(test_key)

    assert result == test_data
    mock_boto3.return_value.get_object.assert_called_once_with(
        Bucket=settings.s3_bucket,
        Key=test_key,
    )


def test_s3_get_log_not_found(s3_storage: S3Storage, mock_boto3: MagicMock) -> None:
    """Test get_log returns None when key doesn't exist."""
    error_response = {"Error": {"Code": "NoSuchKey", "Message": "The specified key does not exist."}}
    mock_boto3.return_value.get_object.side_effect = ClientError(error_response, "GetObject")

    result = s3_storage.get_log("nonexistent-key")

    assert result is None


def test_s3_get_log_error(s3_storage: S3Storage, mock_boto3: MagicMock) -> None:
    """Test get_log handles S3 errors properly."""
    error_response = {"Error": {"Code": "InternalError", "Message": "S3 error"}}
    mock_boto3.return_value.get_object.side_effect = ClientError(error_response, "GetObject")

    with pytest.raises(StorageError, match="Failed to retrieve log from S3"):
        s3_storage.get_log("test-key")
