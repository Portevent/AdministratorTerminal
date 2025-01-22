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

    def test_hard_disconnect(self):
        # Simulates as best as I can a network disconnection or a panic
        def send_dummy():
            requests.post("http://192.168.0.191:8000/new_message/test")

        import multiprocessing

        def setup_listener():
            listener = WebSocketListener(endpoint_url="ws://192.168.0.191:8000/notify?messages")
            listener_thread = listener.initialise()
            listener_thread.start()

        process1 = multiprocessing.Process(target=setup_listener)
        process1.start()

        sleep(1)

        process1.terminate()

        sleep(0.2)

        send_dummy()  # Should trigger an IOError on SpaTch while trying to push the notif to the previously closed ws

        process2 = multiprocessing.Process(target=setup_listener)
        process2.start()

        sleep(1)

        send_dummy()
        send_dummy()
        send_dummy()

        process2.terminate()
