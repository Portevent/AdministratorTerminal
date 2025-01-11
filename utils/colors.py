from enum import IntEnum, auto


class Color(IntEnum):
    CLASSIC = auto()
    PROMPT = auto()
    SUCCESS = auto()
    ERROR = auto()
    DEBUG = auto()
    LOG = auto()
