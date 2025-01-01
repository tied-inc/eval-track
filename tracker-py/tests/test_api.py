"""Tests for the eval-track API endpoints and error handling."""

import pytest
from fastapi.testclient import TestClient

from tracker.main import app


def test_health_check(client: TestClient) -> None:
    """Test the health check endpoint returns OK."""
    response = client.get("/eval-track/health")
    assert response.status_code == 200
    assert response.text == '"OK"'


def test_invalid_secret_key(client: TestClient) -> None:
    """Test that invalid secret key returns 403 with proper error message."""
    response = client.get("/eval-track/traces", headers={"x-eval-tracker-secret-key": "wrong-key"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid secret key"}


def test_missing_secret_key(client: TestClient) -> None:
    """Test that missing secret key returns 403."""
    response = client.get("/eval-track/traces")
    assert response.status_code == 403
    assert response.json() == {"detail": "Missing secret key"}


def test_validation_error(client: TestClient) -> None:
    """Test that invalid request data returns 422 with validation details."""
    response = client.put(
        "/eval-track/traces/test-id",
        json={"invalid": "data"},  # Missing required fields
        headers={"x-eval-tracker-secret-key": app.state.settings.eval_tracker_secret_key.get_secret_value()},
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)  # Validation errors return a list of field errors


@pytest.mark.asyncio
async def test_client_disconnect(client: TestClient) -> None:
    """Test that client disconnection is handled gracefully."""
    with client:
        response = client.get(
            "/eval-track/traces",
            headers={"x-eval-tracker-secret-key": app.state.settings.eval_tracker_secret_key.get_secret_value()},
        )
        assert response.status_code in (200, 499)  # 499 is nginx's code for client disconnected


def test_traces_endpoint(client: TestClient) -> None:
    """Test the traces endpoint with valid secret key."""
    response = client.get(
        "/eval-track/traces",
        headers={"x-eval-tracker-secret-key": app.state.settings.eval_tracker_secret_key.get_secret_value()},
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_put_trace(client: TestClient) -> None:
    """Test putting a trace with valid data."""
    trace_data = {"request": {"method": "GET", "url": "/test"}, "response": {"status_code": 200, "body": "test"}}
    response = client.put(
        "/eval-track/traces/test-trace-id",
        json=trace_data,
        headers={"x-eval-tracker-secret-key": app.state.settings.eval_tracker_secret_key.get_secret_value()},
    )
    assert response.status_code == 204  # No content response for successful put


def test_internal_server_error(client: TestClient) -> None:
    """Test that unhandled exceptions return 500 with proper error format."""
    # Send valid data structure but with test-id to trigger simulated error
    response = client.put(
        "/eval-track/traces/test-id",
        json={"request": {}, "response": {}},  # Valid data structure
        headers={
            "Content-Type": "application/json",
            "x-eval-tracker-secret-key": app.state.settings.eval_tracker_secret_key.get_secret_value(),
        },
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
