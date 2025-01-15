import curses
from abc import ABC, abstractmethod
from typing import List

from flight_deck.elements.element import Element
from flight_deck.client.client import Client


class ClientPage(ABC):

    client: Client | None
    elements: List[Element]

    height: int

    # Index of the selected field
    selectedIndex: int = None

    visible: bool

    def __init__(self):
        self.client = None
        self.elements = []
        self.height = 0
        self.visible = False
        self.selectedIndex = 0

    @property
    def selected_element(self) -> Element:
        """
        Returns the selected Element
        :return: Element
        """
        return self.elements[self.selectedIndex]

    def appendElement(self, element: Element):
        element.y = self.height
        element.setWriter(self.writer, self.moveCursor)
        self.height += element.height
        self.elements.append(element)

    def _display(self):
        """
        Display the page
        """
        for element in self.elements:
            element.display()

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
            self.selected_element.unselect()

        self.selectedIndex = index
        self.selected_element.select()

        
    def nextElement(self):
        if self.selectedIndex < len(self.elements) - 1:
            self.selectElement(self.selectedIndex + 1)

    def previousElement(self):
        if self.selectedIndex > 0:
            self.selectElement(self.selectedIndex - 1)
            
    def onkey(self, char: int):
        if self.selectedIndex is None:
            return

        if char == 0xa:  # Enter key
            self.selected_element.enter()

        elif char == curses.KEY_LEFT:
            self.selected_element.goLeft()

        elif char == curses.KEY_RIGHT:
            self.selected_element.goRight()

        elif char == curses.KEY_UP:
            self.previousElement()

        elif char == curses.KEY_DOWN:
            self.nextElement()

        elif char == curses.KEY_SR:  # Scroll ?up?
            pass
            # self.client.display.scroll(-1)

        elif char == curses.KEY_SF:  # Scroll ?down?
            pass
            # self.client.display.scroll(1)

        elif char == 8:  # Del key
            self.selected_element.delete()

        elif char == curses.KEY_DC:
            self.selected_element.suppr()

        elif chr(char) in self.selected_element.VALID_CHAR:
            self.selected_element.inputChar(chr(char))

    def navigateTo(self, destination: str):
        """
        Navigate to
        :param destination: destination
        """
        if self.client:
            self.client.navigateTo(destination)

    def writer(self, text: str, height: int, start: int, color, refresh):
        if self.visible:
            self.client.display.write(text, height, start, color, refresh)

    def moveCursor(self, x: int, y: int):
        if self.visible:
            self.client.display.moveCursor(x, y)