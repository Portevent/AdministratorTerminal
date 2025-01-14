
from flight_deck.elements.visual_field import VisualField


class TextField(VisualField):
    """
    Simple text field that user can type value into
    """

    max_size: int | None

    insertMode: bool

    def __init__(self, x: int = 0, y: int = 0, width: int | None = None, height: int | None = None,
                name: str = "", label: str | None = None, value: str = "",
                max_size: int | None = None, insertMode: bool = False):
        super().__init__(x, y, width, height, name, label, value,
            valueBackgroundSize=max_size or ((width or self._DEFAUL_WIDTH) - self._VALUE_POSITION))

        self.max_size = max_size
        self.insertMode = insertMode

    def inputChar(self, char: str):
        # If we reached max size, we don't add more character
        if self.max_size and self.current_size >= self.max_size:
            # Except in insert mode (when we just replace char)
            if not (self.insertMode and self.cursorPosition < self.current_size):
                return

        self.value = self.value[:self.cursorPosition] + char + self.value[self.cursorPosition + (1 if self.insertMode else 0):]
        self.cursorPosition += 1

    def goLeft(self):
        if self.cursorPosition > 0:
            self.cursorPosition -= 1

    def goRight(self):
        if self.cursorPosition < self.current_size:
            self.cursorPosition += 1

    def enter(self):
        # TODO : self.page.next()
        pass

    def start(self):
        if self.cursorPosition > 0:
            self.cursorPosition = 0

    def end(self):
        if self.cursorPosition < self.current_size:
            self.cursorPosition = self.current_size

    def delete(self):
        if self.cursorPosition > 0:
            self.value = self.value[:self.cursorPosition-1] + self.value[self.cursorPosition:]
            self.cursorPosition -= 1

    def suppr(self):
        if self.cursorPosition < self.current_size:
            self.value = self.value[:self.cursorPosition] + self.value[self.cursorPosition+1:]
            self.cursorPosition += 0

    @property
    def formatedValue(self) -> str:
        return str(self.value)
