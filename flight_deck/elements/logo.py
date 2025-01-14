from flight_deck.elements.static_element import StaticElement


class Logo(StaticElement):
    """
    //--\\
    ||  ||
    \\__//
    """

    text: str

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, 6, 3)

    def display(self):
        self.write("//--\\\\", 0, 0)
        self.write("||  ||", 1, 0)
        self.write("\\\\__//", 2, 0)

        