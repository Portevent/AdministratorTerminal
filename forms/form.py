from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self


class Form(ABC):
    form_id: int
    form_ver: int

    size_encode_width: int = 2

    @abstractmethod
    def serialise(self) -> str:
        """
        Serialise the form into a base64 string
        :return: base64 string
        """

        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialise(cls, serialised: str) -> Self:
        """
        Serialise the form into a base64 string
        :return: base64 string
        """

        raise NotImplementedError

    @classmethod
    def _serialiseString(cls, buff: str) -> bytes:
        """
        Serialise a string to a buffer, see _deserialiseString for the format
        :param buff: string to serialise
        :return: serialised string
        """

        return len(buff).to_bytes(cls.size_encode_width, 'big') + buff.encode()

    @classmethod
    def _serialiseOptionalString(cls, buff: str | None) -> bytes:
        """
        Serialise a string to a buffer, 0x0000 if string is None
        :param buff: string to serialise
        :return: serialised string
        """

        if buff is None:
            return b'\x00\x00'

        return cls._serialiseString(buff)

    @classmethod
    def _serialiseInt(cls, val: int) -> bytes:
        return val.to_bytes(cls.size_encode_width, 'big')

    @classmethod
    def _deserialiseString(cls, buffer: bytes, start_index: int, optionnal=False) -> (str, int):
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