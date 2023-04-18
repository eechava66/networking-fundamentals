import ipaddress
import logging
from typing import Dict, List, Tuple

from networking.network_devices.device import Device
from networking.network_devices.switch import Switch


class Router:
    routing_table: Dict[str, str]
    mac_table: Dict[str, str]
    _message: Dict
    connected_devices: List[Tuple["Device", int]]

    def __init__(self, mac_address: str, device_name: str, networks=Dict, maximum_devices: int = 5) -> None:
        self.mac_address = mac_address
        self.device_name = device_name
        self.maximum_devices = maximum_devices
        self.mac_table = {}
        self.routing_table = {}
        self.connected_devices = []
        self.flood_identifier = "ffff"
        self.networks = networks

    def connect_device(self, new_device: "Device", port: int):
        if port >= self.maximum_devices:
            raise ValueError(f"{self.device_name} only supports up to {self.maximum_devices} port number")
        logging.debug(f"Connecting device {self.device_name} to {new_device.device_name} using port: {port}")
        if isinstance(new_device, Router):
            for network, ip in new_device.networks.items():
                self.routing_table[network] = ip

        self.connected_devices.append([new_device, port])

    def check_route(self, network, dest_ip):
        network = ipaddress.IPv4Network(network)
        ip = ipaddress.IPv4Address(dest_ip)

        # Check if the IP address belongs to the network mask
        if ip in network:
            logging.info(f"{ip} belongs to the network {network}")
            return True
        else:
            logging.info(f"{ip} does not belong to the network {network}")
            return False

    def send_arp_response(self, destination_mac: str, destination_ip: str):
        network_ip = None
        for network in self.networks.keys():
            if self.check_route(network, destination_ip):
                network_ip = self.networks[network]
        if not network_ip:
            raise ValueError(f"Network for ip: {destination_ip} not present int router {self.device_name}")

        arp_response = {
            "source_ip": network_ip,
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
        self.routing_table[ip] = mac

    @property
    def message(self):
        return self._message

    def arp(self, network_mask, network_ip):
        frame = {
            "source": self.mac_address,
            "dest": "ffff",
            "source_ip": network_ip,
            "curr": self.mac_address,
        }
        for device, port in self.connected_devices:
            if isinstance(device, Switch):
                if device.network == network_mask:
                    logging.info(f"Sending ARP from: {self.device_name} to: {device.device_name} trough port: {port}")
                    device.message = {**frame, "curr": self.mac_address, "port": port}

    @message.setter
    def message(self, message):
        source = message["source"]
        source_ip = message["source_ip"]

        self.add_route(source_ip, source)
        dest = message["dest"]
        print(message)
        if dest == self.flood_identifier:
            self.mac_table[message["curr"]] = message["port"]
            self.send_arp_response(source, source_ip)
        elif dest == self.mac_address and "response" in message and message["data"] == "arp_response":
            logging.info(f"Response received at: {self.device_name} with message: arp_response")
        elif dest == self.mac_address:
            logging.info(f"Route request received at: {self.device_name}")
            network_mask = None
            dest_ip = message["dest_ip"]
            for network in self.networks.keys():
                if self.check_route(network, dest_ip):
                    network_mask = network

            if network_mask:
                logging.info(f"Network {network_mask} belongs to router: {self.device_name}")
                if dest_ip in self.routing_table:
                    logging.info(f"Dest IP: {dest_ip} in: {self.device_name} routing table")
                    for device, port in self.connected_devices:
                        if isinstance(device, Switch):
                            if device.network == network_mask:
                                logging.info(
                                    f"Sending request from: {self.device_name} to: {device.device_name} trough port: {port}"
                                )
                                import time

                                time.sleep(5)
                                device.message = {
                                    **message,
                                    "curr": self.mac_address,
                                    "port": port,
                                    "dest": self.routing_table[dest_ip],
                                }
                else:
                    self.arp(network_mask, self.networks[network_mask])
                    self.message = message

            else:
                logging.info(f"Redirecting to internet!: {network_mask}")
