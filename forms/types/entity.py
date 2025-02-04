
class Entity:
    status: str
    dept: str

    assignedLocation: str


class Replika(Entity):
    modelType: str
    rank: str

    def getID(self) -> str:
        return f"{self.modelType}-{self.assignedLocation}{self.rank}"


class Gestalt(Entity):
    pkz: str

    def getID(self) -> str:
        return self.pkz