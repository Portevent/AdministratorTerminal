from flight_deck.elements.static_element import StaticElement


class Paragraph(StaticElement):
    """
    Simple paragraph element
    """

    text: str

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0, text: str = ""):
        super().__init__(x, y, width, height)
        self.text = text

    def display(self):
        self.write(self.text, 0, 0)
