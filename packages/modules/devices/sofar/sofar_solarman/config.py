from typing import Optional
from helpermodules.auto_str import auto_str

from modules.common.component_setup import ComponentSetup
from ..vendor import vendor_descriptor


class SofarSolarmanConfiguration:
    def __init__(self,
                 ip_address: Optional[str] = None,
                 serial: int = None,
                 port: int = 8899,
                 modbus_id: int = 1):
        self.ip_address = ip_address
        self.serial = serial
        self.port = port
        self.modbus_id = modbus_id


class SofarSolarman:
    def __init__(self,
                 name: str = "SofarSolar (Anbindung per LSW Dongle)",
                 type: str = "sofar_solarman",
                 id: int = 0,
                 configuration: SofarSolarmanConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.vendor = vendor_descriptor.configuration_factory().type
        self.id = id
        self.configuration = configuration or SofarSolarmanConfiguration()


@auto_str
class SofarSolarmanBatConfiguration:
    def __init__(self):
        pass


@auto_str
class SofarSolarmanBatSetup(ComponentSetup[SofarSolarmanBatConfiguration]):
    def __init__(self,
                 name: str = "Sofar Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SofarSolarmanBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SofarSolarmanBatConfiguration())


@auto_str
class SofarSolarmanCounterConfiguration:
    def __init__(self):
        pass


@auto_str
class SofarSolarmanCounterSetup(ComponentSetup[SofarSolarmanCounterConfiguration]):
    def __init__(self,
                 name: str = "Sofar Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SofarSolarmanCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SofarSolarmanCounterConfiguration())


@auto_str
class SofarSolarmanInverterConfiguration:
    def __init__(self):
        pass


@auto_str
class SofarSolarmanInverterSetup(ComponentSetup[SofarSolarmanInverterConfiguration]):
    def __init__(self,
                 name: str = "Sofar Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SofarSolarmanInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SofarSolarmanInverterConfiguration())
