from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Dict

from client.client import Client


class ClientPage(ABC):
    name: str
    client: Client | None
    actions: Dict[str, Callable]

    def __init__(self, name: str, actions: Dict[str, Callable]):
        self.name = name
        self.client = None
        self.actions = actions

    @abstractmethod
    def onkey(self, char: str):
        raise NotImplementedError

    @abstractmethod
    def _display(self):
        """
        Display the page
        :return:
        """
        raise NotImplementedError

    def display(self):
        if self.client is None:
            raise Exception(
                f"Trying to display Client page {self.name} without it being within a client. \n Missing client.addPage(clientPage)")

        self._display()

    def action(self, name, **kwargs):
        self.actions[name](kwargs)
