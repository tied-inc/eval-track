import asyncio
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel

from tracker.tracer import capture_response


class TestResponse(BaseModel):
    value: str


def test_capture_response_sync() -> None:
    """Test capture_response decorator with synchronous function."""

    @capture_response
    def test_func() -> TestResponse:
        return TestResponse(value="test")

    with patch("tracker.client.EvalTrackClient") as mock_client:
        mock_client_instance = mock_client.return_value
        future = asyncio.Future()
        future.set_result(None)
        mock_client_instance.put_trace = AsyncMock(return_value=future)
        result = test_func()

        assert isinstance(result, TestResponse)
        assert result.value == "test"
        mock_client_instance.put_trace.assert_called_once()


@pytest.mark.asyncio
async def test_capture_response_async() -> None:
    """Test capture_response decorator with asynchronous function."""

    @capture_response
    async def test_func() -> TestResponse:
        return TestResponse(value="test")

    with patch("tracker.client.EvalTrackClient") as mock_client:
        mock_client_instance = mock_client.return_value
        future = asyncio.Future()
        future.set_result(None)
        mock_client_instance.put_trace = AsyncMock(return_value=future)
        result = await test_func()

        assert isinstance(result, TestResponse)
        assert result.value == "test"
        mock_client_instance.put_trace.assert_called_once()


def test_capture_response_with_args() -> None:
    """Test capture_response decorator with function arguments."""

    @capture_response
    def test_func(value: str) -> TestResponse:
        return TestResponse(value=value)

    with patch("tracker.client.EvalTrackClient") as mock_client:
        mock_client_instance = mock_client.return_value
        future = asyncio.Future()
        future.set_result(None)
        mock_client_instance.put_trace = AsyncMock(return_value=future)
        result = test_func("test_value")

        assert isinstance(result, TestResponse)
        assert result.value == "test_value"
        mock_client_instance.put_trace.assert_called_once()
