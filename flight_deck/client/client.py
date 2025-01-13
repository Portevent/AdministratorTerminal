import curses
from abc import abstractmethod

from display.display import Display


class Client:
    """
    Client that has a display a windows and listen its input
    """
    
    display: Display

    def __init__(self, display: Display):
        self.display = display

    @abstractmethod
    def onkey(self, key: str):
        raise NotImplementedError

    def start(self):
        self.display.start_listening(self.onkey)

    def __enter__(self):
        self.display.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.display.__exit__(exc_type, exc_val, exc_tb)