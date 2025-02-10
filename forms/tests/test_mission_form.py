import base64
import os
import unittest

from forms.mission_form import MissionForm
from forms.types.entity import Replika


class TestMissionForm(unittest.TestCase):
    @staticmethod
    def genHash() -> str:
        # Stupid hash function to test messages
        return base64.b64encode(os.urandom(256)).decode().replace("/", "").replace("+", "")

    def test_ser_deser(self):
        form = MissionForm()

        dest = Replika()
        dest.modelType = "STAR"
        dest.assignedLocation = self.genHash()[:3]
        dest.rank = self.genHash()[:2]
        dest.status = self.genHash()[:15]
        dest.dept = self.genHash()[:15]

        form.assigned = dest
        form.name = self.genHash()[:25]
        form.location = self.genHash()[:25]
        form.priority = 5
        form.description = self.genHash()[:25]

        serialized = form.serialize()

        assert serialized is not None

        deserialized = form.deserialize(serialized)

        assert deserialized is not None

        assert deserialized.assigned is not None
        assert type(deserialized.assigned) == type(form.assigned)
        assert deserialized.assigned.modelType == form.assigned.modelType
        assert deserialized.assigned.assignedLocation == form.assigned.assignedLocation
        assert deserialized.assigned.rank == form.assigned.rank
        assert deserialized.assigned.status == form.assigned.status
        assert deserialized.assigned.dept == form.assigned.dept
        assert deserialized.assigned.getID() == form.assigned.getID()

        assert deserialized.name == form.name
        assert deserialized.location == form.location
        assert deserialized.priority == form.priority
        assert deserialized.description == form.description