import base64
import os
import unittest
from random import randint

from forms.deserialiser import deserialiseFromEncoded
from forms.report_form import IncidentReportForm
from forms.types.entity import Replika


class TestMissionForm(unittest.TestCase):
    @staticmethod
    def genHash() -> str:
        # Stupid hash function to test messages
        return base64.b64encode(os.urandom(256)).decode().replace("/", "").replace("+", "")

    @classmethod
    def genRandom(cls, model_type="STAR", priority=None, no_proposal=True) -> IncidentReportForm:
        form = IncidentReportForm()

        source = Replika()
        source.modelType = model_type
        source.assignedLocation = cls.genHash()[:3]
        source.rank = cls.genHash()[:2]
        source.status = cls.genHash()[:15]
        source.dept = cls.genHash()[:15]

        dest = Replika()
        dest.modelType = model_type
        dest.assignedLocation = cls.genHash()[:3]
        dest.rank = cls.genHash()[:2]
        dest.status = cls.genHash()[:15]
        dest.dept = cls.genHash()[:15]


        form.source = source
        form.dest = dest
        form.fillingDate = cls.genHash()[:25]
        form.issueTitle = cls.genHash()[:25]
        form.location = cls.genHash()[:25]
        form.priority = priority or randint(1, 5)
        form.issue = cls.genHash()[:25]
        form.proposal = None if no_proposal else cls.genHash()[:25]

        return form

    def test_ser_deser(self):
        form = self.genRandom()

        serialised = form.serialise()

        assert serialised is not None

        deserialised = IncidentReportForm.deserialise(serialised)

        assert deserialised is not None

        # Note: modelType and rank are Replika-specific
        assert deserialised.dest is not None
        assert deserialised.source is not None
        assert type(deserialised.dest) == type(form.dest)
        assert type(deserialised.source) == type(form.source)

        assert deserialised.source.modelType == form.source.modelType
        assert deserialised.source.assignedLocation == form.source.assignedLocation
        assert deserialised.source.rank == form.source.rank
        assert deserialised.source.status == form.source.status
        assert deserialised.source.dept == form.source.dept
        assert deserialised.source.getID() == form.source.getID()

        assert deserialised.dest.modelType == form.dest.modelType
        assert deserialised.dest.assignedLocation == form.dest.assignedLocation
        assert deserialised.dest.rank == form.dest.rank
        assert deserialised.dest.status == form.dest.status
        assert deserialised.dest.dept == form.dest.dept
        assert deserialised.dest.getID() == form.dest.getID()


        assert deserialised.fillingDate == form.fillingDate
        assert deserialised.issueTitle == form.issueTitle
        assert deserialised.priority == form.priority
        assert deserialised.issue == form.issue
        assert deserialised.proposal == form.proposal

    def test_ser_deser2(self):
        form1 = self.genRandom(priority=1, no_proposal=False)
        form2 = self.genRandom(priority=3, no_proposal=False)

        serialised1 = form1.serialise()
        serialised2 = form2.serialise()

        assert serialised1 is not None
        assert serialised2 is not None

        deserialised1 = IncidentReportForm.deserialise(serialised1)
        deserialised2 = IncidentReportForm.deserialise(serialised2)

        assert deserialised1 is not None
        assert deserialised2 is not None

        assert not deserialised1.fillingDate == deserialised2.fillingDate
        assert not deserialised1.issueTitle == deserialised2.issueTitle
        assert not deserialised1.priority == deserialised2.priority
        assert not deserialised1.issue == deserialised2.issue
        assert not deserialised1.proposal == deserialised2.proposal