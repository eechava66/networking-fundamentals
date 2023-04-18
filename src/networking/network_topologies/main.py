import logging

from networking.network_devices import (
    Host,
    Switch,
)
from networking.network_utilities import (
    connect_devices,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#    I will manually manage the networks in order to prevent creating a Network object
#    which will just increase the complexity and won't provide any other benefit.

# 192.168.0.1
default_gateway_network_A = "192.168.0.1"
switch_A = Switch("AA:BB:AB:DD:EE:FF", "192.168.0.5", "SwitchA", 10)
switch_B = Switch("AA:BB:CC:DD:EE:FF", "192.168.0.7", "SwitchB", 10)
host_A = Host("FF:BB:CC:DD:EE:FF", "192.168.0.2", "HostA", default_gateway_network_A)
host_B = Host("BB:BB:FF:DD:EE:FF", "192.168.0.3", "HostB", default_gateway_network_A)
host_C = Host("AA:AA:AA:DD:EE:FF", "192.168.0.4", "HostC", default_gateway_network_A)
host_D = Host("AA:FA:AA:DD:EE:FF", "192.168.0.6", "HostD", default_gateway_network_A)

connect_devices(host_A, switch_B, 0)
connect_devices(switch_B, host_B, 1)
connect_devices(switch_B, host_C, 2)
connect_devices(switch_B, switch_A, 3)
connect_devices(switch_A, host_D, 1)

host_A.send_data("192.168.0.3", "Hi!")
host_D.send_data("192.168.0.2", "Whatsupp")
