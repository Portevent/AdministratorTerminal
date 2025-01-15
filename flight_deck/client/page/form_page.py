from collections.abc import Callable

from flight_deck.elements.field import Field
from flight_deck.elements.button_field import ButtonField
from flight_deck.elements.element import Element
from flight_deck.client.page import ClientPage


class FormPage(ClientPage):

    submitField: ButtonField
    onSubmitCallback: Callable

    def __init__(self, onSubmit: Callable):
        super().__init__()
        self.submitField = ButtonField(name="__submit__", label="SUBMIT", callback=self.submit)
        self.submitField.setWriter(self.writer, self.moveCursor)
        self.elements = [self.submitField]
        self.onSubmitCallback = onSubmit

    def appendElement(self, element: Element):
        element.y = self.height
        element.setWriter(self.writer, self.moveCursor)
        self.height += element.height
        self.elements.insert(len(self.elements) - 2, element)
        self.updateSubmitFieldPosition()

    def updateSubmitFieldPosition(self):
        self.submitField.y = self.height

    def submit(self, *args, **kwargs):
        self.onSubmitCallback({field.name: field.value for field in self.elements if isinstance(field, Field)})
        

