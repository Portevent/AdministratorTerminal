from intercom.db.database import DatabaseInterface

import requests

from intercom.db.errors import ServerUnreachableError, ServerVersionUnrecognisedError, DatabaseError, \
    ServerResponseIncoherent


class SpaTchDatabase(DatabaseInterface):
    def __init__(self, base_url: str):
        if not base_url.endswith('/'):
            base_url += '/'

        super().__init__(base_url)

    def checkConnection(self) -> None:
        """
        Checks if the server is reachable using the / endpoint
        """

        res = requests.get(self.base_url)

        if res.status_code != 200:
            raise ServerUnreachableError

        if res.text != "Hello, world!":
            raise ServerVersionUnrecognisedError

    def sendMessage(self, payload: str) -> int:
        """
        Forwards a message to the server
        :param payload: Message payload
        :return: the id of the message
        """
        res = requests.post(self.base_url + "new_message/" + payload)

        if res.status_code != 200:
            raise DatabaseError(res.text)

        # if not res.text.startswith("N"):
        #     raise ServerResponseIncoherent

        try:
            return int(res.text)
        except ValueError:
            raise DatabaseError("The returned value is not an integer: " + res.text)

    @staticmethod
    def _test_format(message: str) -> bool:
        # Should start with an F (ascii/0x46)
        # F:  01000110
        # cut 010001 10xxxx   |
        # dec     17 32+n     | n <= 31
        # b64      R      C   | C >= f -> z + 0 -> 9 + '+' + /
        # range               | 0x  66   7A  30   39   2B   2F

        char = ord(message[1])
        is_second_in_range = (0x66 <= char <= 0x7a) or (0x30 <= char <= 0x39) or char == 0x2B or char == 0x2F

        if message[0] != 'R' or not is_second_in_range:
            return False

        return True

    @classmethod
    def __format_msg(cls, response: requests.Response) -> str:
        """
        Checks if the server responds corresponds with a serialised form
        """

        if response.status_code != 200:
            raise DatabaseError(response.text)

        if not cls._test_format(response.text):
            raise ServerResponseIncoherent

        return response.text

    def fetchMessage(self, message_id: int, discard_check=False) -> str:
        res = requests.get(self.base_url + "message/" + str(message_id))

        if discard_check:
            return res.text

        return self.__format_msg(res)

    def fetchLastMessage(self, discard_check=False) -> str:
        res = requests.get(self.base_url + "last_message")

        if discard_check:
            return res.text

        return self.__format_msg(res)