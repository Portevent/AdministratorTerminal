from __future__ import annotations

import base64
from typing import Self
from forms.form import Form


class IncidentReportForm(Form):

    form_id = 1
    form_ver = 1

    reportSourceID: str
    location: str
    issueTitle: str
    proposal: str | None
    priority: int

    def serialise(self) -> str:
        serialised = bytes()

        serialised += self.getSignature()

        serialised += self._serialiseString(self.reportSourceID)
        serialised += self._serialiseString(self.location)
        serialised += self._serialiseString(self.issueTitle)
        serialised += self._serialiseString(self.proposal)
        serialised += self._serialiseInt(self.priority)

        return base64.b64encode(serialised).decode()

    @classmethod
    def deserialise(cls, serialised: str, buffer=None) -> Self:
        if buffer is None:
            buffer = base64.b64decode(serialised)

        super().deserialise(serialised, buffer=buffer)


        res = cls()
        last_index = 6

        (res.reportSourceID, size) = cls._deserialiseString(buffer, last_index)
        last_index += size
        (res.location, size) = cls._deserialiseString(buffer, last_index)
        last_index += size
        (res.issueTitle, size) = cls._deserialiseString(buffer, last_index)
        last_index += size
        (res.proposal, size) = cls._deserialiseString(buffer, last_index, optionnal=True)
        last_index += size
        (res.priority, size) = cls._deserialiseInt(buffer, last_index)


        return res