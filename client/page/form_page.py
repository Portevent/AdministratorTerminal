import curses
from collections.abc import Callable
from typing import List, Dict

from client.page.client_page import ClientPage
from field.field import Field

VALID_CHAR = list('/. -\'()<>éèà:^*_')

class FormPage(ClientPage):
    fields: List[Field]

    # Index of the selected field
    selected_index: int = None

    @property
    def selected_field(self) -> Field:
        """
        Returns the selected field
        :return: Field
        """
        return self.fields[self.selected_index]

    def __init__(self, name: str, fields: List[Field], actions: Dict[str, Callable]):
        super().__init__(name, actions)
        self.fields = fields

        for index, field in enumerate(self.fields):
            field.origin_x = 2
            field.origin_y = 1 + 2 * index

    def _display(self):
        """
        Display all field and select the first
        """
        for field in self.fields:
            field.set_writer(self.client.display.display)
            field.set_cursor(self.client.display.moveCursor)
            field.display()

        self.select_field(0)

    def select_field(self, index: int):
        """
        Set the selected field to given index
        :param index: Index of the field
        """
        if self.selected_index:
            self.selected_field.unselect()

        self.selected_index = index
        self.selected_field.select()

    def _next_input(self):
        if self.selected_index < len(self.fields) - 1:
            self.select_field(self.selected_index + 1)

    def _previous_input(self):
        if self.selected_index > 0:
            self.select_field(self.selected_index - 1)

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

        elif chr(char).isalnum() or chr(char) in VALID_CHAR:
            self.selected_field.inputChar(chr(char))
