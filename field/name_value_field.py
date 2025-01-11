from abc import abstractmethod

from client.page.client_page import ClientPage
from field.selectable_field import SelectableField
from utils.colors import Color
from utils.text_formater import TextFormater


class NameValueField(SelectableField):
    """
    Interface that gives name and value to field
    Require field to display them
    """

    PLACEHOLDER_NAME = " "
    DEFAULT_NAME_SIZE = 14
    PLACEHOLDER_VALUE = "_"
    DEFAULT_VALUE_SIZE = 20
    DEFAULT_VALUE_NAME_SPACE = 4

    _name: str
    _value: str
    current_size: int

    placeholder_name: str
    placeholder_value: str

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value
        self.current_size = len(value)
        self.displayValue()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name
        self.displayName()

    def displayName(self):
        self.write(TextFormater.override(self.formatedName, self.placeholder_name), 0, 0, color=Color.CLASSIC)

    def displayValue(self):
        self.write(self.placeholder_value, 0, self.DEFAULT_NAME_SIZE + self.DEFAULT_VALUE_NAME_SPACE, color=Color.CLASSIC)
        self.write(self.formatedValue, 0, self.DEFAULT_NAME_SIZE + self.DEFAULT_VALUE_NAME_SPACE, color=Color.PROMPT)

    @property
    @abstractmethod
    def formatedValue(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def formatedName(self) -> str:
        raise NotImplementedError

    def __init__(self, name: str, x: int, y: int, page: ClientPage, value: str = "",
                 max_value_size: int | None = None):
        super().__init__(x, y, page)
        self._name = name
        self._value = value
        self.current_size = len(value)
        self.placeholder_name = self.PLACEHOLDER_NAME * self.DEFAULT_NAME_SIZE
        self.placeholder_value = self.PLACEHOLDER_VALUE * (max_value_size or self.DEFAULT_VALUE_SIZE)

    def display(self):
        self.displayName()
        self.displayValue()