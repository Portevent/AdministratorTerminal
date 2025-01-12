from __future__ import annotations

import base64
from typing import Self
from forms.form import Form


class MissionForm(Form):

    form_id = 2
    form_ver = 1

    assigned_id: str
    location: str
    name: str
    description: str
    tasks: str | None
    priority: int

    def serialise(self) -> str:
        serialised = bytes()

        serialised += self.getSignature()

        serialised += self._serialiseString(self.assigned_id)
        serialised += self._serialiseString(self.location)
        serialised += self._serialiseString(self.name)
        serialised += self._serialiseString(self.description)
        serialised += self._serialiseString(self.tasks)
        serialised += self._serialiseInt(self.priority)

        return base64.b64encode(serialised).decode()

    @classmethod
    def deserialise(cls, serialised: str, buffer=None) -> Self:
        if buffer is None:
            buffer = base64.b64decode(serialised)

        super().deserialise(serialised, buffer=buffer)


        res = cls()
        last_index = 6

        (res.assigned_id, size) = cls._deserialiseString(buffer, last_index)
        last_index += size
        (res.location, size) = cls._deserialiseString(buffer, last_index)
        last_index += size
        (res.name, size) = cls._deserialiseString(buffer, last_index)
        last_index += size
        (res.description, size) = cls._deserialiseString(buffer, last_index, optionnal=True)
        last_index += size
        (res.tasks, size) = cls._deserialiseString(buffer, last_index, optionnal=True)
        last_index += size
        (res.priority, size) = cls._deserialiseInt(buffer, last_index)


        return res