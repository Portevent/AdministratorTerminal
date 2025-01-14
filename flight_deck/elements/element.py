from abc import abstractmethod, ABC
from typing import Callable

from utils.colors import Color


def SetValidChar(cls, chars: str):
    """
    Class decorator to set valid characters
    """
    cls.VALID_CHAR = list(chars)
    return cls

class Element(ABC):
    """
    Element represent an object on a page
    It has x and y position
    """

    # Display to use
    writer: Callable | None
    cursor: Callable | None

    # Origin point of the display, to write in the right area within the display
    x: int
    y: int

    width: int
    height: int

    # Char that can be entered in this element
    VALID_CHAR = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/. -\'()<>éèà:^*_')

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.writer = None
        self.cursor = None

    def setWriter(self, writer, cursor):
        self.writer = writer
        self.cursor = cursor

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
        if self.writer:
            self.writer(text, self.y + height, self.x + start, color, refresh)

    def moveCursor(self, x: int, y: int):
        """
        Move cursor within the display area
        :param x: X coordinate
        :param y: Y coordinate
        """
        if self.cursor:
            self.cursor(self.x + x, self.y + y)

    @abstractmethod
    def display(self):
        """
        Display the field
        """
        raise NotImplementedError        

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