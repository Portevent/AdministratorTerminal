from typing import Callable, List


class EventListener[CT: Callable[[str], None]]:
    RegisteredCallback = List[CT | None | bool]
    callbacks: List[RegisteredCallback]

    def __init__(self):
        self.callbacks = []

    def register_callback(self, callback: CT) -> int:
        """
        Registers a new callback in the chain
        :param callback: The callback to register
        :return: The id of the registered callback
        """

        self.callbacks.append([callback, True])

        return len(self.callbacks)-1  # Hoping it won't be messed up

    def enable_callback(self, callback_id: int) -> bool:
        """
        Enables a previously disabled callback
        :param callback_id: The id of the callback
        :return: True if successful
        """

        if callback_id >= len(self.callbacks):
            return False

        if self.callbacks[callback_id][0] is None:  # If a function has been deref'd
            return False

        self.callbacks[callback_id][1] = True

        return True

    def disable_callback(self, callback_id: int) -> bool:
        """
        Disables a callback, can be re-enabled later
        :param callback_id: The id of the callback
        :return: True if successful
        """

        if callback_id >= len(self.callbacks):
            return False

        self.callbacks[callback_id][1] = False

        return True

    def remove_callback(self, callback_id: int) -> bool:
        """
        Removes a callback. This can't be undone and the callback won't be able to be re-enabled
        :param callback_id: The id of the callback
        :return: True if successful
        """
        if callback_id >= len(self.callbacks):
            return False

        self.callbacks[callback_id] = [None, False]

        return True

    def on_message(self, message: str):
        """
        On a new event, will propagate to the callback chain
        :param message: The message to propagate
        """

        for (callback, enabled) in self.callbacks:
            if enabled and callback is not None:
                callback(message)
