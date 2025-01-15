class FormatError(Exception):
    pass

class FormDeserialisationError(Exception):
    pass

class WrongFormError(FormDeserialisationError):
    pass

class WrongFormVersionError(FormDeserialisationError):
    pass