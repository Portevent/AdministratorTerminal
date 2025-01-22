from abc import ABC, abstractmethod

from printer.driver import ThermalPrinter
from printer.errors import PrinterException

from forms.form import Form

class Template[T: Form](ABC):
    document: T

    def __init__(self, document: T):
        self.document = document

    def print(self, printer: ThermalPrinter) -> bool:
        """
        Prints the template with the given document.
        :param printer: The printer to use.
        :return: True if successful, False otherwise.
        """

        try:
            self._print(printer)
        except PrinterException:
            return False
        return True

    @abstractmethod
    def _print(self, printer: ThermalPrinter) -> None:
        raise NotImplementedError()