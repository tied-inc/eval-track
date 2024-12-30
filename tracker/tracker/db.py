from abc import ABC, abstractmethod
from typing import Protocol


class AbstractKeyValueStore(ABC):
    @abstractmethod
    async def put_item(self, key: str, value: dict) -> None:
        """Store an item in the key-value store.
        
        Args:
            key: The unique identifier for the item
            value: The data to store
        """
        pass


# Keep as legacy reference until migration is complete
class DynamoDB(AbstractKeyValueStore):
    def __init__(self) -> None: ...

    async def put_item(self, key: str, value: dict) -> None: ...


# Keep as legacy reference until migration is complete
class Redis(AbstractKeyValueStore):
    def __init__(self) -> None: ...


    async def put_item(self, key: str, value: dict) -> None: ...
