from networking.network_devices import (
    Device,
)


def connect_devices(deviceA: Device, deviceB: Device, port: int):
    deviceA.connect_device(deviceB, port)
    deviceB.connect_device(deviceA, port)
