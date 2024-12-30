import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pydantic import BaseModel

from tracker.tracer import capture_response


class TestResponse(BaseModel):
    value: str


def test_capture_response_sync():
    """Test capture_response decorator with synchronous function."""
    @capture_response
    def test_func():
        return TestResponse(value="test")

    with patch("tracker.client.EvalTrackClient") as mock_client:
        mock_client_instance = mock_client.return_value
        result = test_func()
        
        assert isinstance(result, TestResponse)
        assert result.value == "test"
        # Verify background task was added
        mock_client_instance.put_trace.assert_called_once()


@pytest.mark.asyncio
async def test_capture_response_async():
    """Test capture_response decorator with asynchronous function."""
    @capture_response
    async def test_func():
        return TestResponse(value="test")

    with patch("tracker.client.EvalTrackClient") as mock_client:
        mock_client_instance = mock_client.return_value
        result = await test_func()
        
        assert isinstance(result, TestResponse)
        assert result.value == "test"
        # Verify background task was added
        mock_client_instance.put_trace.assert_called_once()


def test_capture_response_with_args():
    """Test capture_response decorator with function arguments."""
    @capture_response
    def test_func(value: str):
        return TestResponse(value=value)

    with patch("tracker.client.EvalTrackClient") as mock_client:
        mock_client_instance = mock_client.return_value
        result = test_func("test_value")
        
        assert isinstance(result, TestResponse)
        assert result.value == "test_value"
        mock_client_instance.put_trace.assert_called_once()
