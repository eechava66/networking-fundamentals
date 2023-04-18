import logging

from networking.network_devices import Host, Router, Switch
from networking.network_utilities import connect_devices

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#    I will manually manage the networks in order to prevent creating a Network object
#    which will just increase the complexity and won't provide any other benefit.

# 192.168.0.0
network = "192.168.0.0/24"
default_gateway_network_A = "192.168.0.1"
switch_A = Switch("AA:BB:AB:DD:EE:FF", "192.168.0.3", "SwitchA", 10, network)
host_A = Host("FF:BB:CC:DD:EE:FF", "192.168.0.2", "HostA", default_gateway_network_A, network)

network_b = "192.168.1.0/24"
default_gateway_network_B = "192.168.1.1"
switch_B = Switch("AF:BB:AB:DD:EE:FF", "192.168.1.5", "SwitchB", 10, network_b)
host_B = Host("FF:FB:CA:DD:EE:FF", "192.168.1.4", "HostB", default_gateway_network_B, network_b)

# 192.168.1.0
router = Router(
    "FF:BA:CC:AD:EE:FF", "Router", networks={network: default_gateway_network_A, network_b: default_gateway_network_B}
)

connect_devices(host_A, switch_A, 0)
connect_devices(router, switch_A, 1)
connect_devices(router, switch_B, 2)
connect_devices(switch_B, host_B, 1)

host_A.send_data("192.168.1.4", "Hey there!")
