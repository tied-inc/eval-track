"""Test configuration for eval-track."""

import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from tracker.main import app
from tracker.settings import get_settings


@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    """Set up test environment variables."""
    os.environ["EVAL_TRACKER_SECRET_KEY"] = "test-secret-key"
    # Force settings reload
    app.state.settings = get_settings()
    yield
    os.environ.pop("EVAL_TRACKER_SECRET_KEY", None)


@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)
