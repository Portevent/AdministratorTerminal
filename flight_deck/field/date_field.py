from typing import override

from client.page.client_page import ClientPage
from field.text_field import TextField
from utils.text_formater import TextFormater


class DateField(TextField):
    """
    Simple Date field
    """

    max_size: int = 8

    def __init__(self, origin_x: int, origin_y: int, page: ClientPage,
                 name: str, value: str, min_size: int | None = None, max_size: int | None = None):
        super().__init__(origin_x=origin_x, origin_y=origin_y, page=page, name=name, value=value, max_size=8)
        self.placeholder_value = "  .  .    "

    def inputChar(self, char: str):
        if not char.isdigit():
            return

        super().inputChar(char)

    @override
    def displayCursor(self):
        self.moveCursor(self.cursor_pos + self.DEFAULT_NAME_SIZE + self.DEFAULT_VALUE_NAME_SPACE + (1 if self.cursor_pos >= 2 else 0) + (1 if self.cursor_pos >= 4 else 0), 0)

    @property
    def formatedValue(self) -> str:
        return TextFormater.override(str(self.value)[0:2], '  ') + "." + TextFormater.override(str(self.value)[2:4], '  ') + "." + str(self.value)[4:8]

