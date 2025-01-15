from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    base_url: str

    @abstractmethod
    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def sendMessage(self, payload: str) -> int:
        raise NotImplemented

    @abstractmethod
    def fetchMessage(self, message_id: int) -> str:
        raise NotImplemented

    @abstractmethod
    def fetchLastMessage(self) -> str:
        raise NotImplemented