from threading import Thread
import rel

import websocket
from websocket import WebSocketApp, WebSocket

from intercom.event.event import EventListener


class WebSocketListener(EventListener):
    endpoint_url: str
    status: int = -2 # 0: closed, 1: open, -1: error, -2: un-initialised
    socket_app: WebSocketApp = None

    def __init__(self, endpoint_url: str):
        super().__init__()

        self.endpoint_url = endpoint_url

    def on_open(self, socket: WebSocket):
        """
        Handles ws open event
        """

        self.status = 1

        print(f"-- on_open@ws: at {self.endpoint_url})")

    def on_close(self, socket: WebSocket, close_code: int, close_msg: str):
        """
        Handles ws close event
        """

        self.status = 0

        # TODO: Add a better log
        print(f"-- on_close@ws: {close_code}, {close_msg}")

    def __on_message(self, socket: WebSocket, message: str):
        """
        Handles the websocket message event, wrapper for super().on_message since WebSocketApp requires
        Callable[[WebSocket, str], Any] and super().on_message is Callable[[str], None]
        """
        super().on_message(message)

    def on_error(self, error):
        """
        Handles ws error event
        """

        self.status = -1

        print(f"-- on_error@ws: {error}")

    def initialise(self, autostart=False) -> Thread:
        """
        Initialise to the ws endpoint
        """
        socket_app = websocket.WebSocketApp(self.endpoint_url,
                                        on_open=self.on_open,
                                        on_close=self.on_close,
                                        on_message=self.__on_message)

        self.socket_app = socket_app
        self.status = 0

        thread = Thread(target=self.run)
        if autostart:
            thread.start()

        return thread

    def run(self):
        if self.status == -2 or self.socket_app is None:
            raise Exception("Is not initialised")

        if self.status != 0:
            raise Exception("Is not closed")

        print("-- run@ws: Starting the ws listener")

        # self.socket_app.run_forever(dispatcher=rel, reconnect=5)
        self.socket_app.run_forever()

    def close(self):
        self.socket_app.close()

        self.status = 0