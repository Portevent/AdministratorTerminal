from abc import abstractmethod, ABC

from flight_deck.elements.element import Element


# @SetValidChar("")
class StaticElement(Element, ABC):
    """
    StaticElement are elements that doesn't respond to user input
    """

    def inputChar(self, char: str):
        pass

    def goLeft(self):
        pass

    def goRight(self):
        pass

    def enter(self):
        pass

    def start(self):
        pass

    def end(self):
        pass

    def delete(self):
        pass

    def suppr(self):
        pass

    def select(self):
        pass

    def unselect(self):
        pass

    @abstractmethod
    def display(self):
        """
        Display the field
        """
        raise NotImplementedError
