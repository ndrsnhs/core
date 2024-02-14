from typing import Optional

from modules.common.component_setup import ComponentSetup


class AzzurroConfiguration:
    def __init__(self, ip_address: Optional[str] = None, port: int = 502):
        self.ip_address = ip_address
        self.port = port


class Azzurro:
    def __init__(self,
                 name: str = "Azzuro/ SofarSolar",
                 type: str = "azzurro_sofarsolar",
                 id: int = 0,
                 configuration: AzzurroConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or AzzurroConfiguration()


class AzzurroInverterConfiguration:
    def __init__(self, modbus_id: int = 1):
        self.modbus_id = modbus_id


class AzzurroInverterSetup(ComponentSetup[AzzurroInverterConfiguration]):
    def __init__(self,
                 name: str = "Azzurro/ Sofarsolar Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: AzzurroInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or AzzurroInverterConfiguration())
