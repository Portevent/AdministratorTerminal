from client.page.form_page import FormPage
from client.simple_client import SimpleClient
from display.display import Display

from field import DateField, TextField, OptionsField, ButtonField


def submit():
    """
    Callback when button is clicked
    """
    data = {form.name: form.value for form in form.fields}

    print(f"Submitted: {data}")

form = FormPage("message", [
        DateField(0,0, None , "Date", "10012025"),
        OptionsField(0, 0, None, "Location", ["Kuisine", "Salon", "Chambre"]),
        TextField(0,0, None , "Object", "", max_size=15),
        ButtonField(0, 0, None, "Send", callback=submit)
    ], actions={})

with SimpleClient([], Display()) as client:
    client.addPage(form)
    client.navigateTo("message")
    client.start()