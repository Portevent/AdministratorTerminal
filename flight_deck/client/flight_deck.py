
def FlightDeckPage(name: str):
    """
    Register a class as a new page, with given name
    :param name: Name of the page
    """
    def registerPage(cls):
        FlightDeck().addPage(cls.__init__(), name)
        return cls
    
    return registerPage

class FlightDeck(SimpleClient, metaclass=Singleton):
    """
    Singleton class that register all pages decorated with @FlightDeckPage
    """
    
    def __init__(self):
        super().__init__()

    