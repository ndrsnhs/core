from typing import Optional

from modules.common.component_setup import ComponentSetup
from ..vendor import vendor_descriptor


class ElmiConfiguration:
    def __init__(self, ip_address: Optional[str] = None, port: int = 502):
        self.ip_address = ip_address
        self.port = port


class Elmi:
    def __init__(self, name: str = "ELMI Hub 400", type: str = "elmi", id: int = 0,
                 configuration: ElmiConfiguration = None):
        self.name = name
        self.type = type
        self.vendor = vendor_descriptor.configuration_factory().type
        self.id = id
        self.configuration = configuration or ElmiConfiguration()


class ElmiBatConfiguration:
    def __init__(self, modbus_id: int = 1):
        self.modbus_id = modbus_id


class ElmiBatSetup(ComponentSetup[ElmiBatConfiguration]):
    def __init__(self, name: str = "ELMI Hub 400 Speicher", type: str = "bat", id: int = 0,
                 configuration: ElmiBatConfiguration = None, **kwargs):
        super().__init__(name, type, id, configuration or ElmiBatConfiguration(), **kwargs)


class ElmiCounterConfiguration:
    def __init__(self, modbus_id: int = 1):
        self.modbus_id = modbus_id


class ElmiCounterSetup(ComponentSetup[ElmiCounterConfiguration]):
    def __init__(self, name: str = "ELMI Hub 400 Zähler", type: str = "counter", id: int = 0,
                 configuration: ElmiCounterConfiguration = None, **kwargs):
        super().__init__(name, type, id, configuration or ElmiCounterConfiguration(), **kwargs)


class ElmiInverterConfiguration:
    def __init__(self, modbus_id: int = 1):
        self.modbus_id = modbus_id


class ElmiInverterSetup(ComponentSetup[ElmiInverterConfiguration]):
    def __init__(self, name: str = "ELMI Hub 400 PV", type: str = "inverter", id: int = 0,
                 configuration: ElmiInverterConfiguration = None, **kwargs):
        super().__init__(name, type, id, configuration or ElmiInverterConfiguration(), **kwargs)
