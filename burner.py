# This script handles the notifications from the server and the printing of those
from time import sleep

from forms.deserialiser import deserialiseFromEncoded
from forms.errors import FormDeserialisationError
from forms.mission_form import MissionForm

from intercom.db.errors import DatabaseError, ServerResponseIncoherent
from intercom.db.spatch import SpaTchDatabase
from intercom.event.websocket import WebSocketListener

from printer.driver import ThermalPrinter
from printer.filter import Filter


def isValidNotification(message: str) -> (bool, int):
    if not message.startswith('N'):
        return False, 0

    try:
        return True, int(message[1:])
    except ValueError:
        return False, 0


def retrieveAndPrint(ws_message: str, database: SpaTchDatabase, printer: ThermalPrinter):
    res, message_id = isValidNotification(ws_message)

    if not res:
        print("There was an issue with the notification format. Full notification is: {}".format(ws_message))

    try:
        retrieved_encoded_form = database.fetchMessage(message_id)
    except ServerResponseIncoherent:
        print("The sent response was incoherent")
        return
    except DatabaseError as e:
        print("A database error occurred: {}".format(e))
        return

    try:
        decoded_form = deserialiseFromEncoded(retrieved_encoded_form)
    except FormDeserialisationError:
        print("Couldn't deserialise the form")
        return

    try:
        filled_template = Filter.templateFromDocument(decoded_form)
        filled_template.print(printer)
    except NotImplementedError:
        print("This form isn't supported yet")
        return
    except Exception as e:
        print("There was an unexpected exception: " + str(e))


if __name__ == "__main__":
    printer_handle = ThermalPrinter.initialise(0x04b8, 0x0202, "TM-T88V")

    ws_notif = WebSocketListener("ws://192.168.0.191:8000/notify?messages")
    ws_thread = ws_notif.initialise()

    db = SpaTchDatabase("http://192.168.0.191:8000/")
    db.checkConnection()

    def callback(message: str) -> None:
        retrieveAndPrint(message, db, printer_handle)

    ws_notif.register_callback(callback)

    ws_thread.start()

    # ----- test

    form = MissionForm()
    form.assigned_id = "ass_test"
    form.location = "loc_test"
    form.name = "subject"
    form.description = "desc example"
    form.tasks = None
    form.priority = 0

    # sleep(5)
    # print("Attempting to send a mission form")

    # serialised_form = form.serialize()

    # db.sendMessage(serialised_form)