from flight_deck.elements.static_element import StaticElement


class Br(StaticElement):
    """
    Add break
    """

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, 1, 1)

    def display(self):
        pass
        