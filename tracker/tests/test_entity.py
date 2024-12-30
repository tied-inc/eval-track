import pytest

from tracker.entity import Trace


def test_trace_creation() -> None:
    """Test that a Trace object can be created with valid data."""
    trace = Trace(
        id="test123",
        request={"data": "input"},
        response={"result": "output"},
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
    )
    assert trace.id == "test123"
    assert trace.request == {"data": "input"}
    assert trace.response == {"result": "output"}
    assert trace.created_at == "2024-01-01T00:00:00Z"
    assert trace.updated_at == "2024-01-01T00:00:00Z"


def test_trace_validation() -> None:
    """Test that Trace validation works correctly."""
    with pytest.raises(ValueError):
        Trace(
            id="test123",
            request=None,  # Should raise error as request is required
            response={"result": "output"},
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        )
