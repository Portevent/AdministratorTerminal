from typing import override, Callable

from flight_deck.elements.visual_field import VisualField, HideCursor


@HideCursor
class ButtonField(VisualField):
    """
    Simple button field that use a callback when it is interacted
    """

    callback: Callable

    def __init__(self, x: int = 0, y: int = 0, width: int | None = None, height: int | None = None,
                name: str = "", label: str | None = None, value: str = "", callback: Callable = None):
        super().__init__(x, y, width, height, name, label, value)
        self.callback = callback

    def inputChar(self, char: str):
        pass

    def goLeft(self):
        pass

    def goRight(self):
        pass

    def enter(self):
        self.callback(self)

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

