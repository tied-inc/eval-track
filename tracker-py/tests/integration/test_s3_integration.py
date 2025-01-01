"""Integration tests for S3 storage backend using localstack."""

import os
import sys
import pytest
import boto3
from botocore.config import Config
from pydantic import SecretStr

# Add tracker package to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from tracker.storage.s3 import S3Storage, StorageError


@pytest.fixture(scope="session")
def s3_client():
    """Create a boto3 client connected to localstack."""
    return boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )


@pytest.fixture(scope="session")
def s3_bucket(s3_client):
    """Create a test bucket."""
    bucket_name = "test-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    return bucket_name


@pytest.fixture
def s3_storage(monkeypatch, s3_bucket):
    """Create S3Storage instance configured for localstack."""
    # Set environment variables for S3 configuration
    monkeypatch.setenv("AWS_ENDPOINT_URL", "http://localhost:4566")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("S3_BUCKET", s3_bucket)
    
    # Override settings for testing
    monkeypatch.setattr("tracker.settings.settings.s3_bucket", s3_bucket)
    monkeypatch.setattr("tracker.settings.settings.s3_region", "us-east-1")
    monkeypatch.setattr("tracker.settings.settings.s3_access_key", SecretStr("test"))
    monkeypatch.setattr("tracker.settings.settings.s3_secret_key", SecretStr("test"))
    
    return S3Storage()


def test_integration_upload_and_retrieve(s3_storage, s3_client, s3_bucket):
    """Test uploading and retrieving data through actual S3 API."""
    key = "test-integration-key"
    data = b"test integration data"

    # Upload data
    s3_storage.upload_log(key, data)

    # Verify data was uploaded correctly
    response = s3_client.get_object(Bucket=s3_bucket, Key=key)
    assert response["Body"].read() == data

    # Retrieve using storage
    retrieved = s3_storage.get_log(key)
    assert retrieved == data


def test_integration_get_nonexistent(s3_storage):
    """Test retrieving non-existent key returns None."""
    assert s3_storage.get_log("nonexistent-key") is None


def test_integration_invalid_bucket(monkeypatch):
    """Test error handling with invalid bucket."""
    # Set environment variables for S3 configuration
    monkeypatch.setenv("AWS_ENDPOINT_URL", "http://localhost:4566")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("S3_BUCKET", "nonexistent-bucket")
    
    # Override settings for testing
    monkeypatch.setattr("tracker.settings.settings.s3_bucket", "nonexistent-bucket")
    monkeypatch.setattr("tracker.settings.settings.s3_region", "us-east-1")
    monkeypatch.setattr("tracker.settings.settings.s3_access_key", SecretStr("test"))
    monkeypatch.setattr("tracker.settings.settings.s3_secret_key", SecretStr("test"))
    
    # Should raise StorageError during initialization since bucket doesn't exist
    with pytest.raises(StorageError) as exc_info:
        storage = S3Storage()
    assert "Not Found" in str(exc_info.value)
