from __future__ import annotations

import base64
from typing import Self

from forms.errors import FormatError, WrongFormError, WrongFormVersionError
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
        serialised = bytearray(["F", self.form_id, self.form_ver])

        serialised += self._serialiseString(self.reportSourceID)
        serialised += self._serialiseString(self.location)
        serialised += self._serialiseString(self.issueTitle)
        serialised += self._serialiseOptionalString(self.proposal)
        serialised += self._serialiseInt(self.priority)

        return base64.b64encode(serialised).decode()

    @classmethod
    def deserialise(cls, serialised: str) -> Self:
        buffer = base64.b64decode(serialised)

        if buffer[0] != b"F":
            raise FormatError("The form data isn't starting with an F :(")

        unpacked_form_id = cls._deserialiseInt(buffer, 1)
        unpacked_form_ver = cls._deserialiseInt(buffer, 1 + cls.size_encode_width)

        if unpacked_form_id != cls.form_id:
            raise WrongFormError

        if unpacked_form_ver != cls.form_ver:
            raise WrongFormVersionError


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