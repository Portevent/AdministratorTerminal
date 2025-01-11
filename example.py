import mission
from client.page.form_page import FormPage
from client.simple_client import SimpleClient
from display.display import Display

from field import DateField, TextField, OptionsField, ButtonField

p = mission.init_printer()

def submit():
    """
    Callback when button is clicked
    """
    values = {form.name: form.value for form in form.fields}
    mission.print_mission_order(p,
                                values['Filling date'][0:2] + "." + values['Filling date'][2:4] + "." + values['Filling date'][4:8],
                                values['Full source ID'],
                                "Staff" if values['Full source ID'] == AGENTS[0] else "Service",
                                "SxeGambette",
                                values['Full dest ID'],
                                values['Object'],
                                values['Location'],
                                values['Description'])

AGENTS = ["PPORTE-E-0972D (Gestalt)", "STAR-L0704 (Replika)"]

form = FormPage("message", [
        DateField(0,0, None , "Filling date", "10012025"),
        OptionsField(0, 0, None, "Full source ID", AGENTS, loop=False),
        OptionsField(0, 0, None, "Full dest ID", AGENTS, loop=False),
        OptionsField(0, 0, None, "Location", ["Kuisine", "Salon", "Chambre"]),
        TextField(0,0, None , "Object", "", max_size=20),
        TextField(0,0, None , "Description", ""),
        ButtonField(0, 0, None, "Send", callback=submit)
    ], actions={})

with SimpleClient([], Display()) as client:
    client.addPage(form)
    client.navigateTo("message")
    client.start()