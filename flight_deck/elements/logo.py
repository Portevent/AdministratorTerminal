class Logo(StaticElement):
    """
    //--\\
    ||  ||
    \\__//
    """"

    text: str

    def __init__(self, page: ClientPage | None = None, x: int = 0, y: int = 0):
        super().__init__(page, x, y, 6, 3)

    def display(self):
        self.write("//--\\", 0, 0)
        self.write("||  ||", 0, 1)
        self.write("\\__//", 0, 2)

        