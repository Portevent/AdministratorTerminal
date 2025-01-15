import unittest

from intercom.event.event import EventListener


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.counter = 0

    def test_register_callback(self):
        event_queue = EventListener()

        assert len(event_queue.callbacks) == 0

        def basicCallback(_: str):
            pass


        callback_id = event_queue.register_callback(basicCallback)

        assert len(event_queue.callbacks) == 1
        assert callback_id == 0

    def test_unregister_callback(self):
        event_queue = EventListener()

        assert len(event_queue.callbacks) == 0
        def basicCallback(_: str):
            pass

        callback_id = event_queue.register_callback(basicCallback)
        event_queue.remove_callback(callback_id)

        assert len(event_queue.callbacks) == 1
        assert event_queue.callbacks[0][0] is None
        assert event_queue.callbacks[0][1] == False

    def test_callback_chain(self):
        event_queue = EventListener()

        self.counter = 0
        def basicCallback(_: str):
            self.counter += 1

        callback_id = event_queue.register_callback(basicCallback)

        assert self.counter == 0
        event_queue.on_message("")
        assert self.counter == 1

        event_queue.on_message("")
        assert self.counter == 2

        event_queue.remove_callback(callback_id)
        event_queue.on_message("")
        assert self.counter == 2

    def test_multiple_callbacks(self):
        event_queue = EventListener()

        self.counter = 0
        self.counter2 = 0

        def basicCallback(_: str):
            self.counter += 1

        def secondBasicCallback(_: str):
            self.counter2 += 1

        cb1_id = event_queue.register_callback(basicCallback)
        cb2_id = event_queue.register_callback(secondBasicCallback)

        assert self.counter == 0
        assert self.counter2 == 0

        event_queue.on_message("")
        assert self.counter == 1
        assert self.counter2 == 1

        event_queue.disable_callback(cb2_id)
        event_queue.on_message("")
        assert self.counter == 2
        assert self.counter2 == 1

        event_queue.enable_callback(cb2_id)
        event_queue.on_message("")
        assert self.counter == 3
        assert self.counter2 == 2