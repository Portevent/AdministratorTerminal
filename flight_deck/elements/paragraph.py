class Paragraph(StaticElement):
    """
    Simple paragraph element
    """"

    text: str

    def __init__(self, page: ClientPage | None = None, x: int = 0, y: int = 0, width: int = 0, height: int = 0, text: str = ""):
        super().__init__(page, x, y, width, height)
        self.text = text

    def display(self):
        self.write(text, 0, 0)
