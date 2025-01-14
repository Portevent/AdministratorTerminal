from typing import override, Callable

from client.page.client_page import ClientPage
from field.name_value_field import NameValueField


@HideCursor
class ButtonField(VisualField):
    """
    Simple button field that use a callback when it is interacted
    """

    callback: Callable

    def __init__(self, page: ClientPage | None = None, x: int = 0, y: int = 0, width: int | None = None, height: int | None = None,
                name: str, label: str | None = None, callback: Callable):
        super().__init__(page, x, y, width, height, name, label)
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
    def formatedLabel(self) -> str:
        return f"[{self.label}]"

