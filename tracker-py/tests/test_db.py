"""Tests for the database abstraction layer."""

import pytest

from tracker.db import AbstractKeyValueStore


class TestKeyValueStore(AbstractKeyValueStore):
    """Test implementation of AbstractKeyValueStore."""

    def __init__(self) -> None:
        """Initialize test store."""
        self.store: dict[str, dict] = {}

    def put_item(self, key: str, value: dict) -> None:
        """Put value for key."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if not isinstance(value, dict):
            raise TypeError("Value must be a dictionary")
        self.store[key] = value


def test_key_value_store_implementation() -> None:
    """Test basic key-value store operations."""
    store = TestKeyValueStore()
    test_data = {"test": "data"}

    # Test put operation
    store.put_item("test-key", test_data)
    assert store.store["test-key"] == test_data


def test_key_value_store_type_validation() -> None:
    """Test that store enforces type constraints."""
    store = TestKeyValueStore()

    with pytest.raises(TypeError):
        store.put_item("test-key", "not-a-dict")  # type: ignore

    with pytest.raises(TypeError):
        store.put_item(123, {"test": "data"})  # type: ignore
