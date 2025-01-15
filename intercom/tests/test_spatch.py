import os
import unittest
import pytest

import base64


from intercom.db.errors import ServerResponseIncoherent
from intercom.db.spatch import SpaTchDatabase


class TestSpaTch(unittest.TestCase):
    @staticmethod
    def genHash() -> str:
        # Stupid hash function to test messages
        return base64.b64encode(os.urandom(256)).decode().replace("/", "").replace("+", "")

    def test_brute_base64_verif(self):
        # Bruteforce try the spatch.SpaTchDatabase._format_msg() function

        F = "F".encode()
        for second_char in range(255):
            test_string = F + chr(second_char).encode()

            b64 = base64.b64encode(test_string)

            assert SpaTchDatabase._test_format(b64.decode())

        assert not SpaTchDatabase._test_format(base64.b64encode("ola".encode()).decode())

#    def test_aigreur(self):
#        self.assertRaises(SpaTchDatabase("http://192.168.0.191:8000"), ServerUrlMalformedException)

    @pytest.mark.timeout(0.2)
    def test_connection(self):
        database = SpaTchDatabase("http://192.168.0.191:8000/")

        database.checkConnection()

    def test_hash(self):
        hash1 = self.genHash()
        hash2 = self.genHash()

        assert hash1 != hash2

    def test_send_message(self):
        database = SpaTchDatabase("http://192.168.0.191:8000/")

        database.checkConnection()

        message1 = self.genHash()
        message1_id = database.sendMessage(message1)

        message2 = self.genHash()
        message2_id = database.sendMessage(message2)

        assert message1 != message2
        assert message1_id != message2_id

    def test_read_message(self):
        database = SpaTchDatabase("http://192.168.0.191:8000/")

        database.checkConnection()

        message1 = self.genHash()
        message1_id = database.sendMessage(message1)

        message2 = self.genHash()
        message2_id = database.sendMessage(message2)

        last_message = database.fetchLastMessage(discard_check=True)
        assert last_message is not None
        assert last_message == message2

        other_message = database.fetchMessage(message1_id, discard_check=True)
        assert other_message is not None
        assert other_message != last_message
        assert other_message == message1

        other_message = database.fetchMessage(message2_id, discard_check=True)
        assert other_message is not None
        assert other_message == last_message