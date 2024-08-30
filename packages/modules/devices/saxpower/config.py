from typing import Optional
from helpermodules.auto_str import auto_str

from modules.common.component_setup import ComponentSetup


@auto_str
class SaxpowerConfiguration:
    def __init__(self, modbus_id: int = 64, ip_address: Optional[str] = None, port: int = 3600):
        self.modbus_id = modbus_id
        self.ip_address = ip_address
        self.port = port


@auto_str
class Saxpower:
    def __init__(self,
                 name: str = "Saxpower",
                 type: str = "saxpower",
                 id: int = 0,
                 configuration: SaxpowerConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SaxpowerConfiguration()


class SaxpowerBatConfiguration:
    def __init__(self):
        pass


class SaxpowerBatSetup(ComponentSetup[SaxpowerBatConfiguration]):
    def __init__(self,
                 name: str = "Saxpower Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SaxpowerBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SaxpowerBatConfiguration())


@auto_str
class SaxpowerCounterConfiguration:
    def __init__(self):
        pass


@auto_str
class SaxpowerCounterSetup(ComponentSetup[SaxpowerCounterConfiguration]):
    def __init__(self,
                 name: str = "Saxpower Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SaxpowerCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SaxpowerCounterConfiguration())
