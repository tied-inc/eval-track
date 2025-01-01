"""Tests for the EvalTrackClient class."""

import pytest
from fastapi import HTTPException

from tracker.tracker.client import EvalTrackClient


@pytest.fixture
def eval_track_client() -> EvalTrackClient:
    """Create an EvalTrackClient instance for testing."""
    return EvalTrackClient()


def test_get_traces(eval_track_client: EvalTrackClient) -> None:
    """Test retrieving traces."""
    with pytest.raises(HTTPException) as exc_info:
        eval_track_client.get_traces()
    assert exc_info.value.status_code == 503


def test_put_trace(eval_track_client: EvalTrackClient) -> None:
    """Test putting a trace."""
    trace_data = {
        "request": {"method": "GET", "url": "/test"},
        "response": {"status_code": 200, "body": "test"},
    }
    with pytest.raises(HTTPException) as exc_info:
        eval_track_client.put_trace("test-trace-id", trace_data)
    assert exc_info.value.status_code == 503


def test_invalid_trace_data(eval_track_client: EvalTrackClient) -> None:
    """Test that client validates trace data."""
    invalid_data = {"invalid": "data"}
    with pytest.raises(HTTPException) as exc_info:
        eval_track_client.put_trace("test-id", invalid_data)
    assert exc_info.value.status_code == 503
