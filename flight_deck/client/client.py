from abc import abstractmethod, ABC

from flight_deck.display import Display


class Client(ABC):
    """
    Client that has a display a windows and listen its input
    """
    
    display: Display | None

    def __init__(self, display: Display | None = None):
        self.display = display

    def __enter__(self):
        if self.display is None:
            raise Exception("Entering Client without specifying a display")

        self.display.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.display.__exit__(exc_type, exc_val, exc_tb)

    def setDisplay(self, display: Display):
        """
        Set the display
        :param display: New display
        """
        self.display = display
        return self

    @abstractmethod
    def start(self, defaultPage: str | None = None):
        raise NotImplementedError

    @abstractmethod
    def onkey(self, key: str):
        raise NotImplementedError
