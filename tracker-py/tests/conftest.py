"""Test configuration and fixtures for eval-track."""

import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from tracker.main import app
from tracker.settings import Settings, settings


@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    """Set up test environment variables."""
    # Store original settings
    original_settings = {
        "eval_tracker_secret_key": settings.eval_tracker_secret_key,
    }

    # Set test environment variables
    os.environ["EVAL_TRACKER_SECRET_KEY"] = "test-secret-key"

    # Create new settings instance to pick up test values
    test_settings = Settings()
    settings.eval_tracker_secret_key = test_settings.eval_tracker_secret_key

    yield

    # Restore original settings
    settings.eval_tracker_secret_key = original_settings["eval_tracker_secret_key"]


@pytest.fixture
def test_client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)
