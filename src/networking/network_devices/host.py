from typing import (
    Dict,
)

from networking.network_devices.device import (
    Device,
)
from networking.network_devices.switch import (
    Switch,
)


class Host(Device):
    """
    Defines a host device.
    """

    routing_table: Dict[str, str]
    mac_table: Dict[str, str]

    def __init__(
        self,
        mac_address: str,
        ip_address: str,
        device_name: str,
        default_gateway: str,
        maximum_devices: int = 3,
    ) -> None:
        super().__init__(mac_address, ip_address, device_name, maximum_devices)
        self.routing_table = {"0.0.0.0/0": default_gateway}
        self.mac_table = {}

    def arp(self):
        frame = {
            "source": self.mac_address,
            "dest": "ffff",
            "source_ip": self.ip_address,
            "current_source": self.mac_address,
        }
        for device, port in self.connected_devices:
            print(f"Sending ARP from: {self.device_name} to: {device.device_name} trough port: {port}")
            device.message = {**frame, "port": port}

    def send_data(self, destination_ip: str, data: str, response: bool = False):
        packet = {
            "source_ip": self.ip_address,
            "dest_ip": destination_ip,
            "source": self.mac_address,
            "current_source": self.mac_address,
            "data": data,
        }
        if response:
            packet["response"] = True
        print(f"Sending data from {self.ip_address} to {destination_ip}")
        if destination_ip in self.routing_table.keys():
            packet["dest"] = self.routing_table[destination_ip]
            for device, port in self.connected_devices:
                if isinstance(device, Switch):
                    print(f"Sending data to: {device.device_name} trough port {port}")
                    device.message = {**packet, "port": port}
                    return
        else:
            self.arp()
            self.send_data(destination_ip, data)

    def send_arp_response(self, destination_mac: str):
        arp_response = {
            "source_ip": self.ip_address,
            "dest": destination_mac,
            "source": self.mac_address,
            "data": "arp_response",
            "current_source": self.mac_address,
            "response": True,
        }
        for device, port in self.connected_devices:
            if isinstance(device, Switch):
                print(
                    f"Sending ARP Response from: {self.device_name} trough switch: {device.device_name} and port: {port} to MAC: {destination_mac}"
                )
                device.message = {**arp_response, "port": port}

    def add_route(self, ip: str, mac: str):
        print(f"Adding route in: {self.device_name} with IP: {ip} and MAC: {mac}")
        self.routing_table[ip] = mac

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        source = message["source"]
        source_ip = message["source_ip"] or None
        self.add_route(source_ip, source)
        dest = message["dest"]
        if dest == self.flood_identifier:
            self.mac_table["current_source"] = message["port"]
            self.send_arp_response(source)
        elif dest == self.mac_address:
            print(f"Message received at: {self.device_name}!! ")
            data = message["data"]
            print(f"Message is: {data}")
            if "response" not in message:
                print(f"Sending response to IP {source_ip}")
                self.send_data(source_ip, "Got your message ;)", True)
        else:
            print(f"Message discarded at: {self.device_name}")
