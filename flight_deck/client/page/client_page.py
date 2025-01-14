from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Dict

from client.client import Client


class ClientPage(ABC):

    name: str
    client: Client | None
    elements: List[Element]

    height: int

    # Index of the selected field
    selectedIndex: int = None

    visible: bool

    def __init__(self, name: str):
        self.name = name
        self.client = None
        self.elements = []
        self.height = 0
        self.visible = False

    @property
    def selected_element(self) -> Element:
        """
        Returns the selected Element
        :return: Element
        """
        return self.elements[self.selectedIndex]

    def appendElement(self, element: Element):
        element.y = self.height
        element.page = self
        self.height += element.height
        self.elements.append(element)

    @abstractmethod
    def onkey(self, char: str):
        raise NotImplementedError

    def _display(self):
        """
        Display the page
        """
        raise NotImplementedError

    def display(self):
        """
        Display the page
        """
        if self.visible:
            self._display()

    def show(self):
        """
        Make this page visible and display it
        """
        self.visible = True
        self.display()

    def hide(self):
        """
        Hide this page
        """
        self.visible = False
        if self.client:
            self.client.display.clear()

    def selectElement(self, index: int):
        """
        Set the selected element to given index
        :param index: Index of the Element
        """
        if self.selectedIndex:
            self.selected_field.unselect()

        self.selectedIndex = index
        self.selected_field.select()

        
    def nextElement(self):
        if self.selectedIndex < len(self.fields) - 1:
            self.selectElement(self.selectedIndex + 1)

    def previousElement(self):
        if self.selectedIndex > 0:
            self.selectElement(self.selectedIndex - 1)
            
    def onkey(self, char: int):

        if char == 0xa:  # Enter key
            self.selected_field.enter()

        elif char == curses.KEY_LEFT:
            self.selected_field.goLeft()

        elif char == curses.KEY_RIGHT:
            self.selected_field.goRight()

        elif char == curses.KEY_UP:
            self._previous_input()

        elif char == curses.KEY_DOWN:
            self._next_input()

        elif char == curses.KEY_SR:  # Scroll ?up?
            pass
            # self.client.display.scroll(-1)

        elif char == curses.KEY_SF:  # Scroll ?down?
            pass
            # self.client.display.scroll(1)

        elif char == 8:  # Del key
            self.selected_field.delete()

        elif char == curses.KEY_DC:
            self.selected_field.suppr()

        elif chr(char) in self.selected_element.VALID_CHAR:
            self.selected_field.inputChar(chr(char))

    def navigateTo(self, destination: str):
        """
        Navigate to
        :param destination: destination
        """
        if self.client:
            self.client.navigateTo(destination)
