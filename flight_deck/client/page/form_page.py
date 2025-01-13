import curses
from collections.abc import Callable
from typing import List, Dict

from client.page.client_page import ClientPage
from field.field import Field


class FormPage(ClientPage):

    submitField: ButtonField
    onSubmitCallback: Callable

    def __init__(self, name: str, onSubmit: Callable):
        super().__init__(name)
        self.submitField = ButtonField(page=self, name="__submit__", label="SUBMIT", callback=self.submit)
        self.elements = [submitField]      
        self.onSubmitCallback = onSubmit

    def appendElement(self, element: Element):
        element.y = self.height
        self.height += element.height
        self.elements.append(element, -1)
        self.updateSubmitFieldPosition()

    def updateSubmitFieldPosition(self):
        self.submitField.y = self.height

    def submit(self):
        self.onSubmitCallback({field.name: field.value for field in self.elements if isintance(field, Field)})
        

