from abc import (
    ABC,
    abstractmethod,
)
import re
from typing import (
    Dict,
    List,
    Tuple,
)


class Device(ABC):
    """Defines a device"""

    _messages: List[Dict]
    connected_devices: List[Tuple["Device", int]]

    def __init__(
        self,
        mac_address: str,
        ip_address: str,
        device_name: str,
        maximum_devices: int = 3,
    ) -> None:
        """MAC (Media Access Control) Address for device, should be composed out of 6 pairs
        of hex numbers  numbers  numbers  numbers  numbers  numbers."""
        self.device_name = device_name
        self.mac_address = mac_address
        self.ip_address = ip_address
        self._messages = []
        self.connected_devices = []
        self.maximum_devices = maximum_devices

    def connect_device(self, new_device: "Device", port: int):
        if port >= self.maximum_devices:
            raise ValueError(
                f"{self.device_name} only supports up to {self.maximum_devices} port number"
            )
        print(
            f"Connecting device {self.device_name} to {new_device.device_name} using port: {port}"
        )
        self.connected_devices.append([new_device, port])

    @property
    @abstractmethod
    def messages(self):
        return self._messages

    @messages.setter
    @abstractmethod
    def messages(self, inbox):
        pass

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
