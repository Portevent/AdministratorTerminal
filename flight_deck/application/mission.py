
AGENTS = ["PPORTE-E-0972D (Gestalt)", "STAR-L0704 (Replika)"]

@FlightDeckPage("mission")
class MissionPage(FormPage):
    """
    Mission form page
    """

    def __init__(self):
        super().__init__(onSubmit=self.sendMission)

        for element in [
            Paragraph(text="New Mission", width=2, height=2),
            DateField(name="filling_date", label="Date", value="10012025"),
            OptionsField(name="full_source_ID", label="Source", values=AGENTS, loop=False),
            OptionsField(name="full_dest_ID", label="Destination", values=AGENTS, loop=False),
            OptionsField(name="location", label="Location", values=["Kuisine", "Salon", "Chambre"]),
            TextField(name="object", max_size=20),
            TextField(name="description"),
            ButtonField(name="back_button", label="Cancel", value="home", callback=self.goBack)
        ]:
            self.appendElement(element)

    def goBack(*agrs, **args):
        self.client.navigateTo("home")

    def sendMission(values: Dict[str, str]):
        print(f"Sending {values}")
        self.client.navigateTo("home")