import curses
from typing import List

from client.page.client_page import ClientPage
from field.name_value_field import NameValueField


class OptionsField(NameValueField):
    """
    Simple option field, where its value can be selected with left and right keys
    """

    _values: List[str]
    values_count: int
    _index: int

    PLACEHOLDER_VALUE = " "

    loop: bool

    has_cursor = False

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, index: int):
        if index >= self.values_count:
            index = 0 if self.loop else (self.values_count - 1)

        if index < 0:
            index = (self.values_count - 1) if self.loop else 0

        self._index = index
        self.value = self.values[self._index]

    @property
    def values(self) -> List[str]:
        return self._values

    @values.setter
    def values(self, values: List[str]):
        self._values = values
        self.values_count = len(self._values)

    def __init__(self, origin_x: int, origin_y: int, page: ClientPage, name: str, values: List[str], default_index: int = 0, loop: bool = True):
        super().__init__(x=origin_x, y=origin_y, page=page, name=name, value="", max_value_size=max(len(x) for x in values)+4)
        self.loop = loop
        self.values = values
        self.index = default_index

    def inputChar(self, char: str):
        pass

    def goLeft(self):
        self.index -= 1

    def goRight(self):
        self.index += 1

    def enter(self):
        pass

    def start(self):
        if self.index > 0:
            self.index = 0

    def end(self):
        if self.index < self.values_count - 1:
            self.index = self.values_count - 1

    def delete(self):
        pass

    def suppr(self):
        pass

    def display(self):
        self.displayName()
        self.displayValue()

    @property
    def formatedName(self) -> str:
        return self.name

    @property
    def formatedValue(self) -> str:
        return f"{'<' if self.loop or self.index > 0 else ' '} {self.value} {'>' if self.loop or self.index < (self.values_count - 1) else ' '}"