import curses
from abc import ABC

from field.field import Field

def HideCursor(original_class):
    """
    Class decorator to hide cursor
    """
    original_class._CURSOR_VISIBLE = False
    return original_class

class VisualField(Field, ABC):
    """
    Improved field to display its label and its value side by side, have a background and selection cursor
    """
    # Note to myself, there is no point to not merge this class with Field. I'm just putting it outside to minimize file length. Not good pratice

    # Class variable to set if cursor is visible or invisible 
    _CURSOR_VISIBLE = True

    # Position and background for label and value
    labelPosition: [int, int]
    valuePosition: [int, int]
    labelBackground: str
    valueBackground: str # Most likely ___________ or ..............

    _focused: bool

    # Default position of value
    _VALUE_POSITION = 20
    _DEFAUL_WIDTH = 42
    _DEFAUL_HEIGTH = 2

    @property
    def focused(self) -> bool:
        return self._focused

    @focused.setter
    def focused(self, focus: bool):
        self._focused = focus
        if self.focused:
            curses.curs_set(1 if self._CURSOR_VISIBLE else 0)
        self.display_focus()

    # Cursor position within the value
    _cursorPosition: int

    @property
    def cursorPosition(self) -> int:
        return self._cursorPosition

    @cursorPosition.setter
    def cursorPosition(self, position: int):
        self._cursorPosition = position
        self.displayCursor()

    def __init__(self, page: ClientPage | None = None, x: int = 0, y: int = 0, width: int | None = None, height: int | None = None,
                name: str, label: str | None = None, value: str = "",
                labelBackgroundSize: int | None = None, valueBackgroundSize: int | None = None):
        super().__init__(page, x, y, width or self._DEFAUL_WIDTH, height or self._DEFAUL_HEIGTH, name, label, value)
        self._generateLabelAndValuePosition(labelBackgroundSize or self.VALUE_POSITION, valueBackgroundSize or len(self.value))
        self.cursorPosition = self.current_size

    def _generateLabelAndValuePosition(self, labelSize: int, valueSize: int):
        self.labelBackground = self._generateLabelBackground(labelSize)
        self.labelPosition = (2, 0)
        self.valueBackground = self._generateValueBackground(valueSize)
        self.valuePosition = (2 + len(labelBackground), 0)

    def _generatelabelBackground(self, size: int):
        return " " * size

    def _generateValueBackground(self, size: int):
        return "." * size

    def select(self):
        self.focused = True

    def unselect(self):
        self.focused = False

    def display(self):
        self.displayFocus()
        self.displayLabel()
        self.displayValue()
        self.displayCursor()

    def displayFocus(self):
        self.write(">" if self.focused else " ", 0, 0)

    def displayLabel(self):
        self.write(self.labelBackground, self.labelPosition[0], self.labelPosition[1], color=Color.CLASSIC)
        self.write(self.formatedLabel, self.labelPosition[0], self.labelPosition[1], color=Color.CLASSIC)

    def displayValue(self):
        self.write(self.valueBackground, self.valuePosition[0], self.valuePosition[1], color=Color.CLASSIC)
        self.write(self.formatedValue, self.valuePosition[0], self.valuePosition[1], color=Color.CLASSIC)

    def displayCursor(self):
        self.moveCursor(self.valuePosition[0] + self.curserPosition, self.valuePosition[1])

    @property
    def formatedLabel(self) -> str:
        return self.label + ": "