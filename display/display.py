import curses, curses.panel
from collections.abc import Callable
from enum import IntEnum, auto


class DisplayColor(IntEnum):
    CLASSIC = auto()
    PROMPT = auto()
    SUCCESS = auto()
    ERROR = auto()
    DEBUG = auto()
    LOG = auto()


class Display:
    """
    Simple curses terminal that display windows
    """
    width: int
    height: int
    message_count: int = 1
    prompt_cursor: int = 0

    # Text variation for each color
    color_variation: dict[DisplayColor, int]

    input_windows: "_CursesWindow"

    listening: bool  # Break bool for listening user input

    def __init__(self):
        """
        Init the windows
        :param client:
        """

        self.stdscr = curses.initscr()
        self.input_windows = self.stdscr
        curses.noecho()
        curses.cbreak()

        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(DisplayColor.CLASSIC, curses.COLOR_WHITE, -1)
            curses.init_pair(DisplayColor.PROMPT, curses.COLOR_BLUE, -1)
            curses.init_pair(DisplayColor.SUCCESS, curses.COLOR_GREEN, -1)
            curses.init_pair(DisplayColor.ERROR, curses.COLOR_RED, -1)
            curses.init_pair(DisplayColor.DEBUG, curses.COLOR_YELLOW, -1)
            curses.init_pair(DisplayColor.LOG, curses.COLOR_WHITE, -1)

        self.color_variation = {DisplayColor.CLASSIC: 0,
                                DisplayColor.PROMPT: 0, DisplayColor.SUCCESS: curses.A_BOLD,
                                DisplayColor.DEBUG: 0, DisplayColor.ERROR: curses.A_BOLD,
                                DisplayColor.LOG: curses.A_ITALIC}

        self.stdscr.keypad(True)
        # self.stdscr.leaveok(True)
        curses.curs_set(1)
        self.width = curses.COLS
        self.height = curses.LINES
        self.listening = False

    def display(self, text: str, height: int, start: int = 0, color: DisplayColor | int = 0, refresh: bool = True):
        """
        Display text at position
        :param text: Text to display
        :param height: Position (vertical)
        :param start: Start position (horizontal)
        :param color: Text variation
        :param refresh: Refresh window
        """
        self.stdscr.addstr(height, start, text,
                           curses.color_pair(color) if isinstance(color, int) else self.color_variation[color])
        if refresh:
            self._refresh()

    def _refresh(self):
        self.stdscr.refresh()

    def moveCursor(self, x: int, y: int, refresh: bool = True):
        """
        Move cursor
        :param x: x position
        :param y: y position
        """
        self.input_windows.move(y, x)
        if refresh:
            self._refresh()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.nocbreak()
        curses.echo()
        self.stdscr.keypad(False)
        curses.endwin()

    def start_listening(self, onkey: Callable):
        """
        Start listening to user input
        """
        self.listening = True
        while self.listening:
            char: int = self.input_windows.getch()

            if char == -1:
                pass
            else:
                onkey(char)

    def clear(self):
        self.input_windows.clear()
