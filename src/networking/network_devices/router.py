from typing import (
    Dict,
)

from networking.network_devices.device import (
    Device,
)


class Switch(Device):
    routing_table: Dict[str, str]

    def __init__(
        self,
        mac_address: str,
        ip_address: str,
        device_name: str,
        maximum_devices: int = 3,
    ) -> None:
        super().__init__(mac_address, ip_address, device_name, maximum_devices)
        self.mac_table = {}

    def flood(self):
        ...

    def forward(self, source_mac: str, data: str, destination_mac: str):
        ...

    def learn(self):
        ...
