from __future__ import annotations

import base64
from typing import Self
from forms.form import Form
from forms.types.entity import Entity


class IncidentReportForm(Form):
    """
    Incident Report, with location, title, priority and an optional proposal
    """

    form_id = 1
    form_ver = 1


    fillingDate: str

    source: Entity

    dest: Entity

    issueTitle: str
    location: str
    issue: str

    proposal: str | None
    priority: int

    def serialise(self) -> str:
        serialised = bytes()

        serialised += self.getSignature()

        # serialised += self._serializeString(self.source.getID())
        serialised += self._serialiseString(self.source.serialise())
        serialised += self._serialiseString(self.source.status)
        serialised += self._serialiseString(self.source.dept)
        # serialised += self._serializeString(self.dest.getID())
        serialised += self._serialiseString(self.dest.serialise())
        serialised += self._serialiseString(self.fillingDate)

        serialised += self._serialiseString(self.issueTitle)
        serialised += self._serialiseString(self.location)
        serialised += self._serialiseString(self.issue)

        serialised += self._serialiseString(self.proposal)
        serialised += self._serialiseInt(self.priority)

        return base64.b64encode(serialised).decode()

    @classmethod
    def _unpack(cls, buffer: bytes, index: int) -> Self:
        res = cls()

        source_serd, index = cls._deserialiseString(buffer, index)
        res.source = Entity.deserialise(source_serd)

        res.sourceStatus, index = cls._deserialiseString(buffer, index)
        res.sourceDept, index = cls._deserialiseString(buffer, index)

        dest_serd, index = cls._deserialiseString(buffer, index)
        res.dest = Entity.deserialise(dest_serd)

        res.fillingDate, index = cls._deserialiseString(buffer, index)

        res.issueTitle, index = cls._deserialiseString(buffer, index)
        res.location, index = cls._deserialiseString(buffer, index)
        res.issue, index = cls._deserialiseString(buffer, index)

        res.proposal, index = cls._deserialiseString(buffer, index, optionnal=True)
        res.priority, index = cls._deserialiseInt(buffer, index)

        return res