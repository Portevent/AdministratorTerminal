import curses
from typing import List, Tuple

from display.display import Display

DEFAULT_NAME = "                    "
DEFAULT_VALUE = "_______________________________"
VALID_CHAR = list('/. -\'()')


def formated_name(name: str) -> str:
    return name + ": " + DEFAULT_NAME[len(name):]


def formated_value(value: str) -> str:
    return value + DEFAULT_VALUE[len(value):]


class Input:
    name: str
    value: str
    selected: bool
    button: bool

    def __init__(self, name: str, value: str = "", selected: bool = False, button: bool = False):
        self.name = name
        self.value = value
        self.selected = selected
        self.button = button

    def __str__(self):
        return f"{'>' if self.selected else ' '} {formated_name(self.name)} {formated_value(self.value) if not self.button else ''}"


class Form(Display):
    # List of inputs and their values
    inputs: List[Input]

    # Index of the selected input
    selected_index: int = None

    @property
    def selected_input(self):
        """
        Returns the selected input
        :return: Input
        """
        return self.inputs[self.selected_index]

    @property
    def prompt(self):
        return self.selected_input.value

    @prompt.setter
    def prompt(self, value):
        self.selected_input.value = value

    def __init__(self, inputs: List[str | Tuple[str, str]], submit):
        super().__init__()

        self.inputs = [Input(input) if isinstance(input, str) else Input(name=input[0], value=input[1]) for input in
                       inputs]
        self.inputs.append(Input("SEND", button=True))

        self._display_inputs()
        self._select_input(0)
        self.submit = submit

    def _display_inputs(self):
        for index in range(len(self.inputs)):
            self.display_input(index, refresh=False)

        self._refresh()

    def display_input(self, index: int, refresh: bool = True, updateCursor: bool = False):

        self._display(str(self.inputs[index]), self.get_input_position(index), refresh=refresh)

        if updateCursor:
            self.updateCursor(refresh=refresh)

    def get_cursor_position(self, index: int):
        """
        Get the Y coordinate of the cursor position.
        :param index: cursor position
        """
        return 25 + index

    def get_input_position(self, index: int):
        """
        Get the X coordinate of the input position.
        :param index: Input index
        """
        return 1 + index * 2

    def _select_input(self, index: int):
        if self.selected_index:
            self.selected_input.selected = False
            self.display_input(self.selected_index, refresh=False)

        self.selected_index = index
        self.prompt_cursor = 0
        self.selected_input.selected = True
        self.display_input(self.selected_index, updateCursor=True)

    def updateCursor(self, refresh: bool = True):
        """
        Auto update the cursor position to selected input and prompt cursor.
        :return:
        """
        self.moveCursor( self.get_cursor_position(self.prompt_cursor), self.get_input_position(self.selected_index),
                        refresh=refresh)

    def _next_input(self):
        if self.selected_index < len(self.inputs) - 1:
            self._select_input(self.selected_index + 1)

    def _previous_input(self):
        if self.selected_index > 0:
            self._select_input(self.selected_index - 1)

    def _delete(self):
        if self.prompt_cursor > 0:
            self.prompt = self.prompt[:self.prompt_cursor - 1] + self.prompt[self.prompt_cursor:]
            self.prompt_cursor -= 1
            self.display_input(self.selected_index, updateCursor=True)

    def _suppr(self):
        self.prompt = self.prompt[:self.prompt_cursor] + self.prompt[self.prompt_cursor + 1:]
        self.display_input(self.selected_index, updateCursor=True)

    def _type(self, char):
        self.prompt = self.prompt[:self.prompt_cursor] + chr(char) + self.prompt[self.prompt_cursor:]
        self.prompt_cursor += 1
        self.display_input(self.selected_index, updateCursor=True)

    def _submit(self):
        self.submit({input.name: input.value for input in self.inputs})

    def input(self, char: int):

        if char == 0xa:  # Enter key
            if self.selected_input.button:
                self._submit()
                self.listening = False
            else:
                self._next_input()

        elif char == curses.KEY_LEFT:
            self.prompt_cursor -= 1
            if self.prompt_cursor < 0:
                self.prompt_cursor = 0

        elif char == curses.KEY_RIGHT:
            self.prompt_cursor += 1
            if self.prompt_cursor > len(self.prompt):
                self.prompt_cursor = len(self.prompt)

        elif char == curses.KEY_UP:
            self._previous_input()

        elif char == curses.KEY_DOWN:
            self._next_input()

        elif char == curses.KEY_SR:  # Scroll ?up?
            pass
            # self.client.display.scroll(-1)

        elif char == curses.KEY_SF:  # Scroll ?down?
            pass
            # self.client.display.scroll(1)

        elif char == 8:  # Del key
            self._delete()

        elif char == curses.KEY_DC:
            self._suppr()

        elif chr(char).isalnum() or chr(char) in VALID_CHAR:
            self._type(char)
