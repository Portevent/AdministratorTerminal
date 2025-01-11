from typing import override, Callable

from client.page.client_page import ClientPage
from field.name_value_field import NameValueField


class ButtonField(NameValueField):
    """
    Simple button field that use a callback when it is interacted
    """

    has_cursor = False
    callback: Callable

    def __init__(self, origin_x: int, origin_y: int, page: ClientPage, name: str, callback: Callable):
        super().__init__(name=name, x=origin_x, y=origin_y, page=page, value="pristine")
        self.callback = callback

    def inputChar(self, char: str):
        pass

    def goLeft(self):
        pass

    def goRight(self):
        pass

    def enter(self):
        self.value = "clicked"
        self.callback()

    def start(self):
        pass

    def end(self):
        pass

    def delete(self):
        pass

    def suppr(self):
        pass

    @override
    def displayValue(self):
        pass

    @property
    def formatedValue(self) -> str:
        return ""

    @property
    def formatedName(self) -> str:
        return f"[{self.name}]"

