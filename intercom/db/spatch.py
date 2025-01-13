from intercom.db.database import DatabaseInterface

import requests

from intercom.db.errors import ServerUnreachableError, ServerVersionUnrecognisedError, DatabaseError


class SpaTchDatabase(DatabaseInterface):
    def __init__(self, base_url):
        if not base_url.endswith('/'):
            base_url += '/'

        super().__init__(base_url)

    def checkConnection(self):
        res = requests.get(self.base_url)

        if res.status_code != 200:
            raise ServerUnreachableError

        if res.text != "Hello, world!":
            raise ServerVersionUnrecognisedError

    def sendMessage(self, payload: str) -> int:
        res = requests.post(self.base_url + "new_message/" + payload)

        if res.status_code != 200:
            raise DatabaseError(res.text)

        try:
            return int(res.text)
        except ValueError:
            raise DatabaseError("The returned value is not an integer: " + res.text)

    @staticmethod
    def __format_msg(response: requests.Response) -> str:
        if response.status_code != 200:
            raise DatabaseError(response.text)

        return response.text

    def fetchMessage(self, message_id: int) -> str:
        res = requests.get(self.base_url + "message/" + str(message_id))

        return self.__format_msg(res)

    def fetchLastMessage(self) -> str:
        res = requests.get(self.base_url + "last_message")

        return self.__format_msg(res)