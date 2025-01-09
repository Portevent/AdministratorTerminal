from typing import Dict

from display.form import Form

import mission

p = mission.init_printer()


def send(values: Dict[str, str]):
    # print(values)
    mission.print_mission_order(p, values['Filling date'], values['Full source ID'], "status", "dpt", values['Full dest ID'], values['Object'], values['Location'], values['Description'])

with Form([
    ["Filling date", "09.01.2025"],
    "Full source ID",
    "Full dest ID",
    ["Object", "No Object"],
    "Location",
    "Description"], submit=send) as display:
    display.start_listening()
