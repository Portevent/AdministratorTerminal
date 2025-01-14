from abc import abstractmethod

from client.page.client_page import ClientPage
from field.selectable_field import SelectableField
from utils.colors import Color
from utils.text_formater import TextFormater


class Field(Element):
    """
    Element that has an name, a label and a value
    """

    name: str
    _label: str
    _value: str
    current_size: int = 0 # Size of the current value
    
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value
        self.current_size = len(value)
        self.displayValue()

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label
        self.displayLabel()

    def __init__(self, page: ClientPage | None = None, x: int = 0, y: int = 0, width: int = 0, height: int = 0, name: str, label: str | None = None, value: str = ""):
        super().__init__(page, x, y, width, height)
        self.name = name
        self.label = label or self.name
        self.value = value

    def display(self):
        self.displaylabel()
        self.displayValue()

    @abstractmethod
    def displayLabel(self):
        raise NotImplementedError

    @abstractmethod
    def displayValue(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def formatedLabel(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def formatedValue(self) -> str:
        raise NotImplementedError