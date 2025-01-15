


class DatabaseError(Exception):
    pass

class ServerResponseIncoherent(DatabaseError):
    pass

class ServerUnreachableError(DatabaseError):
    pass

class ServerVersionUnrecognisedError(DatabaseError):
    pass