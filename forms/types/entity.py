import re
from typing import Self

MODELS = ["MNHR", "FKLR", "STCR", "STAR", "ARAR", "LSTR", "ADLR", "EULR", "KLBR"]

class Entity:
    status: str
    dept: str

    assignedLocation: str

    def getID(self) -> str:
        return "undefined"

    @staticmethod
    def fromID(id: str) -> "Entity":
        if id[:4] in MODELS:
            return Replika._fromID(id)

        if re.match("[A-Z]*-", id[:10]): #????? tkt
            return Gestalt._fromID(id)

        return Entity()


class Replika(Entity):
    modelType: str
    rank: str

    @classmethod
    def _fromID(cls, id: str) -> Self:
        res = Replika()

        res.modelType = id[:4]
        res.assignedLocation = id[5:8]
        res.rank = id[8:10]

    def getID(self) -> str:
        return f"{self.modelType}-{self.assignedLocation}{self.rank}"


class Gestalt(Entity):
    pkz: str

    @classmethod
    def _fromID(cls, id: str) -> Self:
        return cls()

    def getID(self) -> str:
        return self.pkz