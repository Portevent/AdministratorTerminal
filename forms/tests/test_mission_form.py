import base64
import os
import unittest
from random import randint

from forms.deserialiser import deserialiseFromEncoded
from forms.mission_form import MissionForm
from forms.types.entity import Replika


class TestMissionForm(unittest.TestCase):
    @staticmethod
    def genHash() -> str:
        # Stupid hash function to test messages
        return base64.b64encode(os.urandom(256)).decode().replace("/", "").replace("+", "")

    def genRandom(self, model_type="STAR", priority=None) -> MissionForm:
        form = MissionForm()

        dest = Replika()
        dest.modelType = model_type
        dest.assignedLocation = self.genHash()[:3]
        dest.rank = self.genHash()[:2]
        dest.status = self.genHash()[:15]
        dest.dept = self.genHash()[:15]

        form.assigned = dest
        form.name = self.genHash()[:25]
        form.location = self.genHash()[:25]
        form.priority = priority or randint(1, 5)
        form.description = self.genHash()[:25]

        return form

    def test_ser_deser(self):
        form = self.genRandom()

        serialised = form.serialise()

        assert serialised is not None

        deserialised = MissionForm.deserialise(serialised)

        assert deserialised is not None

        # Note: modelType and rank are Replika-specific
        assert deserialised.assigned is not None
        assert type(deserialised.assigned) == type(form.assigned)
        assert deserialised.assigned.modelType == form.assigned.modelType
        assert deserialised.assigned.assignedLocation == form.assigned.assignedLocation
        assert deserialised.assigned.rank == form.assigned.rank
        assert deserialised.assigned.status == form.assigned.status
        assert deserialised.assigned.dept == form.assigned.dept
        assert deserialised.assigned.getID() == form.assigned.getID()

        assert deserialised.name == form.name
        assert deserialised.location == form.location
        assert deserialised.priority == form.priority
        assert deserialised.description == form.description

    def test_ser_deser2(self):
        form1 = self.genRandom(priority=1)
        form2 = self.genRandom(priority=3)

        serialised1 = form1.serialise()
        serialised2 = form2.serialise()

        assert serialised1 is not None
        assert serialised2 is not None

        deserialised1 = MissionForm.deserialise(serialised1)
        deserialised2 = MissionForm.deserialise(serialised2)

        assert deserialised1 is not None
        assert deserialised2 is not None

        assert not deserialised1.name == deserialised2.name
        assert not deserialised1.location == deserialised2.location
        assert not deserialised1.priority == deserialised2.priority
        assert not deserialised1.description == deserialised2.description