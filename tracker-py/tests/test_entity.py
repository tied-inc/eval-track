"""Tests for the entity models."""

import pytest
from pydantic import ValidationError

from tracker.entity import Trace


def test_trace_creation() -> None:
    """Test creating a valid Trace object."""
    trace_data = {
        "id": "test-id",
        "request": {"method": "GET", "url": "/test"},
        "response": {"status_code": 200, "body": "test"},
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
    }
    trace = Trace(**trace_data)
    assert trace.request == trace_data["request"]
    assert trace.response == trace_data["response"]
    assert trace.id == trace_data["id"]
    assert trace.created_at == trace_data["created_at"]
    assert trace.updated_at == trace_data["updated_at"]


def test_trace_validation() -> None:
    """Test that Trace validates required fields."""
    base_data = {"id": "test-id", "created_at": "2024-01-01T00:00:00Z", "updated_at": "2024-01-01T00:00:00Z"}

    with pytest.raises(ValidationError):
        Trace(**base_data, request={})  # Missing response field

    with pytest.raises(ValidationError):
        Trace(**base_data, response={})  # Missing request field

    with pytest.raises(ValidationError):
        empty_data: dict[str, object] = {}
        Trace(**empty_data)  # Missing all required fields
