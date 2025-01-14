from typing import override

from flight_deck.elements.text_field import TextField
from flight_deck.elements.element import SetValidChar
from utils.text_formater import TextFormater

# @SetValidChar(chars="0123456789")
class DateField(TextField):
    """
    Simple Date field
    """

    def __init__(self, x: int = 0, y: int = 0, width: int | None = None, height: int | None = None,
                name: str = "", label: str | None = None, value: str = "00112222"):
        super().__init__(x, y, width, height, name, label, value, max_size=8, insertMode=True)

    def inputChar(self, char: str):
        if not char.isdigit():
            return

        super().inputChar(char)

    @override
    def displayCursor(self):
        self.moveCursor(self.valuePosition[0] + self.cursorPosition + (1 if self.cursorPosition >= 2 else 0) + (1 if self.cursorPosition >= 4 else 0), self.valuePosition[1])

    @property
    def formatedValue(self) -> str:
        return TextFormater.override(str(self.value)[0:2], '  ') \
        + "." + TextFormater.override(str(self.value)[2:4], '  ') \
        + "." + TextFormater.override(str(self.value)[4:8], '    ') 

