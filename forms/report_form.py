from __future__ import annotations

import base64
from typing import Self
from forms.form import Form


class IncidentReportForm(Form):
    """
    Incident Report, with location, title, priority and an optional proposal
    """

    form_id = 1
    form_ver = 1

    reportSourceID: str
    location: str
    issueTitle: str
    proposal: str | None
    priority: int

    def serialize(self) -> str:
        serialised = bytes()

        serialised += self.getSignature()

        serialised += self._serializeString(self.reportSourceID)
        serialised += self._serializeString(self.location)
        serialised += self._serializeString(self.issueTitle)
        serialised += self._serializeString(self.proposal)
        serialised += self._serialiseInt(self.priority)

        return base64.b64encode(serialised).decode()

    @classmethod
    def _unpack(cls, buffer: bytes, index: int) -> Self:
        res = cls()

        res.reportSourceID, index = cls._deserializeString(buffer, index)
        res.location, index = cls._deserializeString(buffer, index)
        res.issueTitle, index = cls._deserializeString(buffer, index)
        res.proposal, index = cls._deserializeString(buffer, index, optionnal=True)
        res.priority, index = cls._deserializeInt(buffer, index)

        return res