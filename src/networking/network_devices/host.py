import ipaddress
import logging
from typing import Dict

from networking.network_devices.device import Device
from networking.network_devices.switch import Switch


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
        network: str,
        maximum_devices: int = 3,
    ) -> None:
        super().__init__(mac_address, ip_address, device_name, maximum_devices)
        self.routing_table = {"0.0.0.0/0": default_gateway}
        self.default_gateway = default_gateway
        self.mac_table = {}
        self.network = network

    def arp(self):
        frame = {
            "source": self.mac_address,
            "dest": "ffff",
            "source_ip": self.ip_address,
            "curr": self.mac_address,
        }
        for device, port in self.connected_devices:
            logging.info(f"Sending ARP from: {self.device_name} to: {device.device_name} trough port: {port}")
            device.message = {**frame, "port": port}

    def send_data_to_switch(self, packet):
        for device, port in self.connected_devices:
            if isinstance(device, Switch):
                logging.info(f"Sending data to: {device.device_name} trough port {port}")
                device.message = {**packet, "port": port}
                return

    def send_data(self, destination_ip: str, data: str, response: bool = False):
        packet = {
            "source_ip": self.ip_address,
            "dest_ip": destination_ip,
            "source": self.mac_address,
            "curr": self.mac_address,
            "data": data,
        }
        if response:
            packet["response"] = True
        logging.info(f"Sending data from {self.ip_address} to {destination_ip}")
        if destination_ip in self.routing_table.keys():
            packet["dest"] = self.routing_table[destination_ip]
            self.send_data_to_switch(packet)
        elif not self.belongs_to_network(destination_ip) and self.default_gateway in self.mac_table:
            packet["dest"] = self.mac_table[self.default_gateway]
            self.send_data_to_switch(packet)
        else:
            self.arp()
            self.send_data(destination_ip, data)

    def send_arp_response(self, destination_mac: str):
        arp_response = {
            "source_ip": self.ip_address,
            "dest": destination_mac,
            "source": self.mac_address,
            "data": "arp_response",
            "curr": self.mac_address,
            "response": True,
        }
        for device, port in self.connected_devices:
            if isinstance(device, Switch):
                logging.info(
                    f"Sending ARP Response from: {self.device_name} trough switch: {device.device_name} and port: {port} to MAC: {destination_mac}"
                )
                device.message = {**arp_response, "port": port}
                return

    def add_route(self, ip: str, mac: str):
        logging.info(f"Adding route in: {self.device_name} with IP: {ip} and MAC: {mac}")
        self.mac_table[ip] = mac

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        source = message["source"]
        source_ip = message["source_ip"]
        self.add_route(source_ip, source)
        dest = message["dest"]
        if dest == self.flood_identifier:
            self.mac_table[message["curr"]] = message["port"]
            self.send_arp_response(source)
        elif dest == self.mac_address:
            logging.info(f"Message received at: {self.device_name}!! ")
            data = message["data"]
            logging.info(f"Message is: {data}")
            if "response" not in message:
                logging.info(f"Sending response to IP {source_ip}")
                self.send_data(source_ip, "Got your message ;)", True)
        else:
            logging.info(f"Message discarded at: {self.device_name}")

    def belongs_to_network(self, dest_ip):
        network = ipaddress.IPv4Network(self.network)
        ip = ipaddress.IPv4Address(dest_ip)

        # Check if the IP address belongs to the network mask
        if ip in network:
            logging.info(f"{ip} belongs to the network {network}")
            return True
        else:
            logging.info(f"{ip} does not belong to the network {network}")
            return False
