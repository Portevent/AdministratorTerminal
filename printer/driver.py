from __future__ import annotations

from escpos.printer import Usb


class ThermalPrinter(Usb):
    @staticmethod
    def initialise(vid: int, pid: int, profile: str = "TM-T88V") -> ThermalPrinter:
        """
        Initialise our printer :D
        """
        return ThermalPrinter(vid, pid, 0, profile=profile)