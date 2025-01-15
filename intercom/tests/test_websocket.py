import unittest
from time import sleep

import requests

from intercom.event.websocket import WebSocketListener


class TestWebSocket(unittest.TestCase):
    def test_tests(self):
        assert True

    @staticmethod
    def isValidAnswer(ans: str) -> bool:
        if not ans.startswith('N'):
            return False

        try:
            message_id = int(ans[1:])
        except ValueError:
            return False

        return True

    def test_no_connection(self):
        listener = WebSocketListener(endpoint_url="ws://192.168.0.191:8000/notify?meages")
        listener_thread = listener.initialise()
        listener_thread.start()

        sleep(0.3)
        assert listener.status == 0

        listener.close()

        sleep(0.3)
        assert listener.status == 0

    def test_connection(self):
        listener = WebSocketListener(endpoint_url="ws://192.168.0.191:8000/notify?messages")
        listener_thread = listener.initialise()
        listener_thread.start()

        sleep(0.3)
        assert listener.status == 1

        listener.close()

        sleep(0.3)
        assert listener.status == 0

    def test_manual_message(self):
        listener = WebSocketListener(endpoint_url="ws://192.168.0.191:8000/notify?messages")
        listener_thread = listener.initialise()
        listener_thread.start()

        sleep(0.3)
        assert listener.status == 1

        self.calls: [str] = []
        def callback(message: str):
            self.calls.append(message)

        assert len(self.calls) == 0

        listener.register_callback(callback)

        assert len(self.calls) == 0

        requests.post("http://192.168.0.191:8000/new_message/test")
        sleep(0.3)

        assert len(self.calls) == 1
        assert self.isValidAnswer(self.calls[0])