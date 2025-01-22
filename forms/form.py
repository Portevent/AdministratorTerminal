from __future__ import annotations

import base64
from abc import ABC, abstractmethod
from typing import Self

from forms.errors import FormatError, WrongFormError, WrongFormVersionError


class Form(ABC):
    """
    Abstract Form with ID and Version
    """
    form_id: int
    form_ver: int

    size_encode_width: int = 2

    def getSignature(self) -> bytes:
        """
        Get the signature of this form
        :return: the signature
        """
        return b"F" + self._serialiseInt(self.form_id) + self._serialiseInt(self.form_ver)

    @abstractmethod
    def serialize(self) -> str:
        """
        Serialise the form into a base64 string
        :return: base64 string
        """

        raise NotImplementedError

    @classmethod
    def deserialize(cls, serialised: str) -> Self:
        """
        Deserialise a string into a Form
        :param serialised: base64 string
        :return: Form
        """

        buffer = base64.b64decode(serialised)

        return cls.deserialiseFromBytes(buffer)

    @classmethod
    def deserialiseFromBytes(cls, buffer: bytes) -> Self:
        signature_ok, index = cls.checkSignature(buffer)

        return cls._unpack(buffer, index)

    @classmethod
    @abstractmethod
    def _unpack(cls, buffer: bytes, index: int) -> Self:
        """
        Unpack Form from bytes, starting at index
        :param buffer: buffer
        :param index: position to start
        :return: Form
        """
        raise NotImplementedError

    @classmethod
    def _getSignature(cls, buffer: bytes = None, index: int = 0) -> (int, int, int):
        if chr(buffer[index]) != "F":
            raise FormatError("The form data isn't starting with an F :(")

        index += 1
        unpacked_form_id, index = cls._deserializeInt(buffer, index)
        unpacked_form_ver, index = cls._deserializeInt(buffer, index)

        return unpacked_form_id, unpacked_form_ver, index

    @classmethod
    def tryGetSignature(cls, buffer: bytes = None, index: int = 0) -> (bool, int, int, int):
        try:
            return True, *cls._getSignature(buffer, index)
        except FormatError:  # FormatError and deserialise Error
            return False, 0, 0, index

    @classmethod
    def checkSignature(cls, buffer: bytes = None, index: int = 0) -> (bool, int):
        """
        Check signature
        :param buffer: buffer to decode
        :param index: index to start at
        :return: bool if signature is okay, and integer for the index where the signature ends
        """

        unpacked_form_id, unpacked_form_ver, index = cls._getSignature(buffer, index)

        if unpacked_form_id != cls.form_id:
            raise WrongFormError

        if unpacked_form_ver != cls.form_ver:
            raise WrongFormVersionError

        return True, index

    @classmethod
    def _serializeString(cls, buff: str | None) -> bytes:
        """
        Serialise a string to a buffer, see _deserialiseString for the format, 0x0000 if string is None
        :param buff: string to serialise
        :return: serialised string
        """

        if buff is None:
            return b'\x00\x00'

        return len(buff).to_bytes(cls.size_encode_width, 'big') + buff.encode()

    @classmethod
    def _serialiseInt(cls, val: int) -> bytes:
        return val.to_bytes(cls.size_encode_width, 'big')

    @classmethod
    def _deserializeString(cls, buffer: bytes, start_index: int, optionnal: bool = False) -> (str, int):
        """
        Deserialise a buffer formatted as 0xaaaabbbbbbbbbbbbbbbb (aaaa being the length of the bbbbbbb section)
        :param buffer: buffer to deserialise
        :param start_index: start index
        :return: deserialised string and the new index
        """

        size, index = cls._deserializeInt(buffer, start_index)
        if optionnal and size == 0:
            return None, index

        return buffer[index:index + size].decode(), index + size

    @classmethod
    def _deserializeInt(cls, buffer: bytes, start_index: int) -> (int, int):
        """
        Deserialise a int
        :param buffer: buffer to deserialise
        :param start_index: start index
        :return: deserialised int and the new index
        """
        return int.from_bytes(buffer[start_index:start_index + cls.size_encode_width],
                              byteorder="big"), start_index + cls.size_encode_width

    # TODO: Decide if we want that
    # @abstractmethod
    # def createPage(self):
    #     raise NotImplementedError