from abc import abstractmethod, ABC
from collections.abc import Callable

from client.page.client_page import ClientPage
from utils.colors import Color


class Field(ABC):
    """
    Field represent a field than can be interacted with
    It has it own area where it can write text into
    """

    # Display to use
    page: ClientPage

    # Origin point of the display, to write in the right area within the display
    origin_x: int
    origin_y: int

    # Callables to write text & move cursor
    _writer: Callable | None
    _cursor: Callable | None

    def __init__(self, x: int, y: int, page: ClientPage):
        self.origin_x = x
        self.origin_y = y
        self.page = page
        self._writer = None
        self._cursor = None

    def set_writer(self, writer: Callable | None):
        self._writer = writer

    def set_cursor(self, cursor: Callable | None):
        self._cursor = cursor

    def write(self, text: str, height: int, start: int = 0, color: Color | int = 0, refresh: bool = True):
        """
        Write text in the field area
        :param text:
        :param height:
        :param start:
        :param color:
        :param refresh:
        :return:
        """
        if self._writer:
            self._writer(text, self.origin_y + height, self.origin_x + start, color, refresh)

    def moveCursor(self, x: int, y: int):
        """
        Move cursor within the display area
        :param x: X coordinate
        :param y: Y coordinate
        """
        if self._cursor:
            self._cursor(self.origin_x + x, self.origin_y + y)

    @abstractmethod
    def inputChar(self, char: str):
        """
        Character is inputted in the field
        :param char: Inputed char
        """
        raise NotImplementedError

    @abstractmethod
    def goLeft(self):
        """
        Going left is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def goRight(self):
        """
        Going right is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def enter(self):
        """
        Enter key is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def start(self):
        """
        Start key is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def end(self):
        """
        End key is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        """
        Delete key is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def suppr(self):
        """
        Suppr key is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def select(self):
        """
        Field is being selected
        """
        raise NotImplementedError

    @abstractmethod
    def unselect(self):
        """
        Field is being unselected
        """
        raise NotImplementedError

    @abstractmethod
    def display(self):
        """
        Display the field
        """
        raise NotImplementedError