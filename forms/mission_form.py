from __future__ import annotations

import base64
from typing import Self
from forms.form import Form
from forms.types.entity import Entity


class MissionForm(Form):
    """
    Mission Form, with an assigned, a location, a name, a description and a priority. May have a task.
    """
    form_id = 2
    form_ver = 1

    assigned: Entity
    location: str
    name: str
    description: str
    tasks: str | None = None
    priority: int

    def serialize(self) -> str:
        serialised = bytes()

        serialised += self.getSignature()

        # serialised += self._serializeString(self.assigned.serialise())
        serialised += self._serializeString(self.assigned.serialise())
        serialised += self._serializeString(self.location)
        serialised += self._serializeString(self.name)
        serialised += self._serializeString(self.description)
        serialised += self._serializeString(self.tasks)
        serialised += self._serialiseInt(self.priority)

        return base64.b64encode(serialised).decode()

    @classmethod   
    def _unpack(cls, buffer: bytes, index: int) -> Self:
        res = cls()
        
        dest_serd, index = cls._deserializeString(buffer, index)
        res.assigned = Entity.deserialise(dest_serd)

        res.location, index = cls._deserializeString(buffer, index)
        res.name, index = cls._deserializeString(buffer, index)
        res.description, index = cls._deserializeString(buffer, index, optionnal=True)
        res.tasks, index = cls._deserializeString(buffer, index, optionnal=True)
        res.priority, index = cls._deserializeInt(buffer, index)

        return res