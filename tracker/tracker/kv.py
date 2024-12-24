from abc import ABC, abstractmethod


class AbstractKeyValueStore(ABC):
    @abstractmethod
    def put_item(self, key: str, value: dict) -> None:
        pass


class DynamoDB(AbstractKeyValueStore):
    def __init__(self) -> None: ...

    def put_item(self, key: str, value: dict) -> None: ...


class Redis(AbstractKeyValueStore):
    def __init__(self) -> None: ...

    def put_item(self, key: str, value: dict) -> None: ...
