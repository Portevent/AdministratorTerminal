import curses
from typing import override

from client.page.client_page import ClientPage
from field.name_value_field import NameValueField


class TextField(NameValueField):
    """
    Simple text field that user can type value into
    """

    min_size: int | None
    max_size: int | None
    _cursor_pos: int
    placeholder_name: str
    placeholder_value: str

    @override
    def select(self):
        super().select()
        self.displayCursor()

    @property
    def cursor_pos(self) -> int:
        return self._cursor_pos

    @cursor_pos.setter
    def cursor_pos(self, cursor_pos: int):
        self._cursor_pos = cursor_pos
        self.displayCursor()

    def __init__(self, origin_x: int, origin_y: int, page: ClientPage,
                 name: str, value: str, min_size: int | None = None, max_size: int | None = None):
        super().__init__(x=origin_x, y=origin_y, page=page, name=name, value=value, max_value_size=max_size)

        self.min_size = min_size
        self.max_size = max_size

        self.cursor_pos = 0

    def inputChar(self, char: str):
        if self.max_size and self.current_size >= self.max_size:
            return

        self.value = self.value[:self.cursor_pos] + char + self.value[self.cursor_pos:]
        self.cursor_pos += 1

    def goLeft(self):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1

    def goRight(self):
        if self.cursor_pos < self.current_size:
            self.cursor_pos += 1

    def enter(self):
        pass

    def start(self):
        if self.cursor_pos > 0:
            self.cursor_pos = 0

    def end(self):
        if self.cursor_pos < self.current_size:
            self.cursor_pos = self.current_size

    def delete(self):
        if self.cursor_pos > 0:
            self.value = self.value[:self.cursor_pos-1] + self.value[self.cursor_pos:]
            self.cursor_pos -= 1

    def suppr(self):
        if self.cursor_pos < self.current_size:
            self.value = self.value[:self.cursor_pos] + self.value[self.cursor_pos+1:]
            self.cursor_pos += 0

    def display(self):
        super().display()
        self.displayCursor()

    def displayCursor(self):
        self.moveCursor(self.cursor_pos + self.DEFAULT_NAME_SIZE + self.DEFAULT_VALUE_NAME_SPACE, 0)

    @property
    def formatedValue(self) -> str:
        return str(self.value)

    @property
    def formatedName(self) -> str:
        return str(self.name)

