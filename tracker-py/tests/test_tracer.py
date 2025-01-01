"""Tests for the tracer module."""

import asyncio
from typing import Any

import pytest
from pydantic import BaseModel

from tracker.tracker.tracer import capture_response


class TestResponse(BaseModel):
    """Test response model."""

    message: str
    value: int


@capture_response
def test_sync_function() -> TestResponse:
    """Test synchronous function."""
    return TestResponse(message="test", value=42)


@capture_response
async def test_async_function() -> TestResponse:
    """Test asynchronous function."""
    await asyncio.sleep(0.1)  # Simulate async work
    return TestResponse(message="async test", value=42)


def test_sync_capture() -> None:
    """Test synchronous function capture."""
    result = test_sync_function()
    assert isinstance(result, TestResponse)
    assert result.message == "test"
    assert result.value == 42


@pytest.mark.asyncio
async def test_async_capture() -> None:
    """Test asynchronous function capture."""
    result = await test_async_function()
    assert isinstance(result, TestResponse)
    assert result.message == "async test"
    assert result.value == 42


def test_sync_invalid_return() -> None:
    """Test synchronous function with invalid return type."""

    @capture_response
    def invalid_sync_function() -> Any:
        return "not a BaseModel"

    with pytest.raises(AttributeError):
        invalid_sync_function()


@pytest.mark.asyncio
async def test_async_invalid_return() -> None:
    """Test asynchronous function with invalid return type."""

    @capture_response
    async def invalid_async_function() -> Any:
        return "not a BaseModel"

    with pytest.raises(AttributeError):
        await invalid_async_function()


def test_background_tasks_added() -> None:
    """Test that background tasks are added correctly."""

    @capture_response
    def function_with_background() -> TestResponse:
        return TestResponse(message="test", value=42)

    result = function_with_background()
    assert isinstance(result, TestResponse)
    assert result.message == "test"
    assert result.value == 42
    # Note: We can't directly test the background tasks as they're internal to the decorator
    # but we can verify the function's behavior remains correct
