from abc import abstractmethod, ABC

from flight_deck.display import Display


class Client(ABC):
    """
    Client that has a display a windows and listen its input
    """
    
    display: Display

    def __init__(self, display: Display):
        self.display = display

    def __enter__(self):
        self.display.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.display.__exit__(exc_type, exc_val, exc_tb)

    @abstractmethod
    def start(self, defaultPage: str | None = None):
        raise NotImplementedError

    @abstractmethod
    def onkey(self, key: str):
        raise NotImplementedError
