import curses
from abc import ABC

from field.field import Field


class SelectableField(Field, ABC):
    """
    Make a field have a '>' behind it when it is selected
    """


    # Class variable to set cursor
    has_cursor = True

    def select(self):
        curses.curs_set(1 if self.has_cursor else 0)
        self.write(">", 0, -2)

    def unselect(self):
        self.write(" ", 0, -2)