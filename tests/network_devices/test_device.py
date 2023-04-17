import pytest
from networking.network_devices.device import Device


def test_device_mac_address():
    with pytest.raises(TypeError):
        device = Device("not-a-valid-mac", "192.168.0.1", "Test Device")

    device = Device("AA:BB:CC:DD:EE:FF", "192.168.0.1", "Test Device")
    assert device.mac_address == "AA:BB:CC:DD:EE:FF"


def test_device_ip_address():
    with pytest.raises(TypeError):
        device = Device("AA:BB:CC:DD:EE:FF", "not-a-valid-ip", "Test Device")

    device = Device("AA:BB:CC:DD:EE:FF", "192.168.0.1", "Test Device")
    assert device.ip_address == "192.168.0.1"
