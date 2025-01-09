from typing import Dict

from display.form import Form

def send(values: Dict[str, str]):
    print(values)

with Form([
    ["Filling date", "09.01.2025"],
    "Full source ID",
    "Full dest ID",
    ["Object", "No Object"],
    "Location",
    "Description"], submit=send) as display:
    display.start_listening()
