import re
from typing import Self

MODELS = ["MNHR", "FKLR", "STCR", "STAR", "ARAR", "LSTR", "ADLR", "EULR", "KLBR"]

class Entity:
    status: str = ""
    dept: str = ""

    assignedLocation: str = ""

    def getID(self) -> str:
        return "undefined"

    def serialise(self):
        return f"{self.getID()}${self.status}${self.dept}"

    @staticmethod
    def fromID(id: str) -> "Entity":
        if id[:4] in MODELS:
            return Replika._fromID(id)

        if re.match("[A-Z]*-", id[:10]): #????? tkt
            return Gestalt._fromID(id)

        return Entity()

    @classmethod
    def deserialise(cls, ser: str) -> "Entity":
        ser_spl = ser.split("$")

        res = cls.fromID(ser_spl[0])
        res.status = ser_spl[1]
        res.dept = ser_spl[2]

        return res


class Replika(Entity):
    modelType: str = ""
    rank: str = ""

    @classmethod
    def _fromID(cls, id: str) -> Self:
        res = cls()

        res.modelType = id[:4]
        res.assignedLocation = id[5:8]
        res.rank = id[8:10]

        return res


    def getID(self) -> str:
        return f"{self.modelType}-{self.assignedLocation}{self.rank}"


class Gestalt(Entity):
    pkz: str

    @classmethod
    def _fromID(cls, id: str) -> Self:
        return cls()

    def getID(self) -> str:
        return self.pkz