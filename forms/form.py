from __future__ import annotations

import base64
from abc import ABC, abstractmethod
from typing import Self

from forms.errors import FormatError, WrongFormError, WrongFormVersionError


class Form(ABC):


    form_id: int
    form_ver: int

    size_encode_width: int = 2


    def getSignature(self):
        """
        Get the signature of this form
        :return: the signature
        """
        return bytearray(["F", self.form_id, self.form_ver])

    @abstractmethod
    def serialise(self) -> str:
        """
        Serialise the form into a base64 string
        :return: base64 string
        """

        raise NotImplementedError

    @classmethod
    def deserialise(cls, serialised: str, buffer: bytes = None) -> Self:
        """
        Serialise the form into a base64 string
        :return: base64 string
        """

        if buffer is None:
            buffer = base64.b64decode(serialised)

        if buffer[0] != b"F":
            raise FormatError("The form data isn't starting with an F :(")

        unpacked_form_id = cls._deserialiseInt(buffer, 1)
        unpacked_form_ver = cls._deserialiseInt(buffer, 1 + cls.size_encode_width)

        if unpacked_form_id != cls.form_id:
            raise WrongFormError

        if unpacked_form_ver != cls.form_ver:
            raise WrongFormVersionError

    @classmethod
    def _serialiseString(cls, buff: str | None) -> bytes:
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
    def _deserialiseString(cls, buffer: bytes, start_index: int, optionnal: bool = False) -> (str, int):
        """
        Deserialise a buffer formatted as 0xaaaabbbbbbbbbbbbbbbb (aaaa being the length of the bbbbbbb section)
        :param buffer: buffer to deserialise
        :param start_index: start index
        :return: deserialised string and the new index
        """

        next_size = int.from_bytes(buffer[start_index:start_index + cls.size_encode_width], byteorder="big")
        if optionnal and next_size == 0:
            return None, 0

        res = buffer[start_index + cls.size_encode_width:start_index + cls.size_encode_width + next_size].decode()

        return res, next_size + cls.size_encode_width

    @classmethod
    def _deserialiseInt(cls, buffer: bytes, start_index: int) -> int:
        return int.from_bytes(buffer[start_index:start_index + cls.size_encode_width], byteorder="big")


    # TODO: Decide if we want that
    # @abstractmethod
    # def createPage(self):
    #     raise NotImplementedError