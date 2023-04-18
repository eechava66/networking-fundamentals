from typing import (
    Dict,
    List,
)

from networking.network_devices.device import (
    Device,
)


class Switch(Device):
    mac_table: Dict[str, str]
    flood_identifier: str

    def __init__(
        self,
        mac_address: str,
        ip_address: str,
        device_name: str,
        maximum_devices: int = 3,
    ) -> None:
        super().__init__(mac_address, ip_address, device_name, maximum_devices)
        self.mac_table = {}
        self.flood_identifier = "ffff"

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        source = message["current_source"]
        port = message["port"]
        dest = message["dest"]
        self.learn(source, port)
        if dest in self.mac_table.keys():
            self.forward(message)
        else:
            self.flood(message)

    def flood(self, frame: Dict):
        for device, port in self.connected_devices:
            if device.mac_address == frame["current_source"]:
                continue
            print(f"Flooding from {self.device_name} to: {device.device_name} using port {port}")
            device.message = {
                **frame,
                "port": port,
                "current_source": self.mac_address,
            }

    def forward(self, message: Dict):
        dest = message["dest"]
        for device, port in self.connected_devices:
            if device.mac_address == dest:
                print(f"Forwarding from {self.device_name} to :{dest} using port {port}")
                device.message = message
                return

        print(self.mac_table)
        raise ValueError("There was an error in Forward operation")

    def learn(self, source: str, port: int):
        print(f"Learning from {self.device_name} - Adding MAC: {source} using port: {port}")
        self.mac_table[source] = port
        print(self.mac_table)
