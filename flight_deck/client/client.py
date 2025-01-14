import curses
from abc import abstractmethod

from display.display import Display


class Client:
    """
    Client that has a display a windows and listen its input
    """
    
    display: Display
    pages: Dict[str, ClientPage]
    current_page_name: str | None

    def __init__(self, display: Display):
        self.display = display
        self.pages = {}
        self.current_page_name = None

    def __enter__(self):
        self.display.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.display.__exit__(exc_type, exc_val, exc_tb)

    def start(self, defaultPage: str | None = None):
        if defaultPage:
            self.navigateTo(defaultPage)
            
        self.display.start_listening(self.onkey)

    @property
    def current_page(self) -> ClientPage | None:
        if self.current_page_name is None:
            return None
        return self.pages[self.current_page_name]

    def addPage(self, page: ClientPage):
        page.client = self
        self.pages[page.name] = page

    def onkey(self, key: str):
        if self.current_page:
            self.current_page.onkey(key)

    def navigateTo(self, destination: str):
        if self.current_page:
            self.current_page.hide()

        self.current_page_name = destination
        self.current_page.display()
