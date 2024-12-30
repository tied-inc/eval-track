from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import Request, Response

from tracker.middleware import api_access_log_middleware, secret_key_middleware


@pytest.mark.asyncio
async def test_secret_key_middleware_valid_key() -> None:
    """Test secret key middleware with valid key."""
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"x-eval-tracker-secret-key": "test-key"}

    mock_response = Response(content="test")
    mock_call_next = AsyncMock(return_value=mock_response)

    with patch("tracker.settings.settings") as mock_settings:
        mock_settings.eval_tracker_secret_key = "test-key"
        response = await secret_key_middleware(mock_request, mock_call_next)

    assert response == mock_response
    mock_call_next.assert_called_once_with(mock_request)


@pytest.mark.asyncio
async def test_secret_key_middleware_invalid_key() -> None:
    """Test secret key middleware with invalid key."""
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"x-eval-tracker-secret-key": "wrong-key"}

    mock_call_next = AsyncMock()

    with patch("tracker.settings.settings") as mock_settings:
        mock_settings.eval_tracker_secret_key = "test-key"
        response = await secret_key_middleware(mock_request, mock_call_next)

    assert response.status_code == 403
    assert response.body == b"Invalid secret key"
    assert isinstance(response, Response)
    mock_call_next.assert_not_called()


@pytest.mark.asyncio
async def test_api_access_log_middleware() -> None:
    """Test API access log middleware."""
    mock_request = MagicMock(spec=Request)
    mock_request.method = "GET"
    mock_request.url.path = "/test"
    mock_request.query_params = {}
    mock_request.is_disconnected = AsyncMock(return_value=False)

    mock_response = Response(content="test")
    mock_call_next = AsyncMock(return_value=mock_response)

    response = await api_access_log_middleware(mock_request, mock_call_next)

    assert response == mock_response
    mock_call_next.assert_called_once_with(mock_request)


@pytest.mark.asyncio
async def test_api_access_log_middleware_disconnected() -> None:
    """Test API access log middleware with client disconnection."""
    mock_request = MagicMock(spec=Request)
    mock_request.method = "GET"
    mock_request.url.path = "/test"
    mock_request.query_params = {}
    mock_request.is_disconnected = AsyncMock(return_value=True)

    mock_response = Response(content="test")
    mock_call_next = AsyncMock(return_value=mock_response)

    response = await api_access_log_middleware(mock_request, mock_call_next)

    assert response == mock_response
    mock_call_next.assert_called_once_with(mock_request)
