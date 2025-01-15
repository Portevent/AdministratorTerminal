from flight_deck import FlightDeck, CursesDisplay

with FlightDeck().setDisplay(CursesDisplay()) as client:

    # Start client
    client.start("home")