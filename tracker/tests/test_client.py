import pytest
from unittest.mock import patch, MagicMock

from tracker.client import EvalTrackClient


@patch("httpx.Client")
def test_get_traces_success(mock_client) -> None:
    """Test successful retrieval of traces."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"traces": []}
    mock_client.return_value.__enter__.return_value.get.return_value = mock_response

    client = EvalTrackClient()
    result = client.get_traces()

    assert result == {"traces": []}
    mock_client.return_value.__enter__.return_value.get.assert_called_once()


@patch("httpx.Client")
def test_get_traces_error(mock_client) -> None:
    """Test error handling in get_traces."""
    mock_client.return_value.__enter__.return_value.get.side_effect = Exception("Network error")

    client = EvalTrackClient()
    result = client.get_traces()

    assert result == {}


@patch("httpx.Client")
def test_put_trace_success(mock_client) -> None:
    """Test successful trace update."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_client.return_value.__enter__.return_value.put.return_value = mock_response

    client = EvalTrackClient()
    client.put_trace("test123", {"data": "test"})

    mock_client.return_value.__enter__.return_value.put.assert_called_once()


@patch("httpx.Client")
def test_put_trace_error(mock_client) -> None:
    """Test error handling in put_trace."""
    mock_client.return_value.__enter__.return_value.put.side_effect = Exception("Network error")

    client = EvalTrackClient()
    client.put_trace("test123", {"data": "test"})  # Should not raise exception
