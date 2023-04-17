import re


class Device:
    """Defines a device"""

    def __init__(self, mac_address: str, ip_address: str, device_name: str) -> None:
        """MAC (Media Access Control) Address for device, should be composed out of 6 pairs
        of hex numbers  numbers  numbers  numbers  numbers  numbers."""
        self.device_name = device_name
        self.mac_address = mac_address
        self.ip_address = ip_address

    @property
    def mac_address(self):
        """
        MAC (Media Access Control) Address for device, should be composed out of 6 pairs of
        hex numbers.
        """
        return self._mac_address

    @property
    def ip_address(self):
        """
        IP (Internet Protocol) Address for device, should be
         composed out of 4 octets which can go from 0 to 255
        """
        return self._ip_address

    @mac_address.setter
    def mac_address(self, value):
        pattern = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
        match = re.match(pattern, value)
        if not bool(match):
            raise TypeError(f"Not valid MAC Address for device :{self.device_name}")
        self._mac_address = value

    @ip_address.setter
    def ip_address(self, value):
        pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        match = re.match(pattern, value)
        if not bool(match):
            raise TypeError(f"Not valid ip Address for device :{self.device_name}")
        self._ip_address = value
