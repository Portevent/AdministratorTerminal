from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import IntEnum, auto


class DisplayColor(IntEnum):
    CLASSIC = auto()
    PROMPT = auto()
    SUCCESS = auto()
    ERROR = auto()
    DEBUG = auto()
    LOG = auto()


class Display(ABC):

    @abstractmethod
    def write(self, text: str, height: int, start: int = 0, color: DisplayColor | int = 0, refresh: bool = True):
        """
        Display text at position
        :param text: Text to display
        :param height: Position (vertical)
        :param start: Start position (horizontal)
        :param color: Text variation
        :param refresh: Refresh window
        """
        raise NotImplementedError

    @abstractmethod
    def moveCursor(self, x: int, y: int, refresh: bool = True):
        """
        Move cursor
        :param x: x position
        :param y: y position
        """
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    def start_listening(self, onkey: Callable):
        """
        Start listening to user input
        :param onkey: callback
        """
        raise NotImplementedError
