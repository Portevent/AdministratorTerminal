from typing import Dict

from flight_deck.elements.field import Field
from flight_deck.client.client import Client
from flight_deck.display import Display
from flight_deck.client import ClientPage


class SimpleClient(Client):
    """
    Client that has a display a windows and listen its input
    """

    pages: Dict[str, ClientPage]
    current_page_name: str | None

    def __init__(self, display: Display):
        super().__init__(display)
        self.pages = {}
        self.current_page_name = None

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

    def navigateTo(self, destination: str | Field):
        if self.current_page:
            self.current_page.hide()

        self.current_page_name = destination if isinstance(destination, str) else destination.value
        self.current_page.show()
