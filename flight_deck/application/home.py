
@FlightDeckPage("home")
class HomePage(ClientPage):
    """
    Home page
    """

    def __init__(self):
        super().__init__()

        self.appendElement(Paragraph(text="Flight Deck", width=2, height=2))
        self.appendElement(Logo())
        self.appendElement(Br())
        self.appendElement(ButtonField(name="new_mission", label="New Mission", value="mission", callback=FlightDeck().navigateTo))
