from typing import Dict

# import mission
from flight_deck import Client, ClientPage, FormPage, Display, CursesDisplay
from flight_deck.client.simple_client import SimpleClient
from flight_deck.elements import Paragraph, Logo, DateField, TextField, OptionsField, ButtonField

# p = mission.init_printer()


def send_print_order(values: Dict[str, str]):
    """
    Callback when button is clicked
    """
    print(values)

AGENTS = ["PPORTE-E-0972D (Gestalt)", "STAR-L0704 (Replika)"]


with SimpleClient(CursesDisplay()) as client:

    # Create the home page
    home = ClientPage(name="home")

    home.appendElement(Paragraph(text="Flight Deck", width=2, height=2))
    home.appendElement(Logo())
    home.appendElement(ButtonField(name="new_mission", label="New Mission", value="mission", callback=client.navigateTo))


    # Create the form page
    mission = FormPage(name="mission", onSubmit=send_print_order)

    elements = [
        Paragraph(text="New Mission", width=2, height=2),
        DateField(name="filling_date", label="Date", value="10012025"),
        OptionsField(name="full_source_ID", label="Source", values=AGENTS, loop=False),
        OptionsField(name="full_dest_id", label="Destination", values=AGENTS, loop=False),
        OptionsField(name="location", label="Location", values=["Kuisine", "Salon", "Chambre"]),
        TextField(name="object", max_size=20),
        TextField(name="description"),
        ButtonField(name="back_button", label="Cancel", value="home", callback=client.navigateTo)
    ]

    for element in elements:
        mission.appendElement(element)


    # Register pages
    client.addPage(home)
    client.addPage(mission)

    # Start client
    client.start("home")