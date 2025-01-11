from pathlib import Path
from typing import Dict, List

from client.client import Client
from client.page.client_page import ClientPage
from client.page.form_page import FormPage
from display.display import Display


class SimpleClient(Client):
    """
    Simple client that has a home screen and basic logic
    """
    pages: Dict[str, ClientPage]

    current_page_name: str | None

    @property
    def current_page(self) -> ClientPage | None:
        if self.current_page_name is None:
            return None
        return self.pages[self.current_page_name]

    def __init__(self, pages: List[ClientPage], display: Display):
        super().__init__(display)
        self.pages = {}
        self.current_page_name = None

    def addPage(self, page: ClientPage):
        page.client = self
        self.pages[page.name] = page

    def onkey(self, key: str):
        self.current_page.onkey(key)

    def navigateTo(self, name: str):
        if self.current_page:
            self.display.clear()

        self.current_page_name = name
        self.current_page.display()

    def registerPage(self, path: Path):

        with path.open("r") as stream:
            data = yaml.safe_load(stream)

            name = path.stem

            match data["type"]:
                case "text":
                    raise NotImplementedError
                case "title":
                    raise NotImplementedError
                case "form":
                    self._addPage(self.registerFormPage(name, data))

    def registerFormPage(self, name: str, data):
        fields = []
        for field in data["fields"]:
            pass

        return FormPage(name, fields=[], actions={})