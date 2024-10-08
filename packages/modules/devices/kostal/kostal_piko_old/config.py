from typing import Optional

from helpermodules.auto_str import auto_str
from modules.common.component_setup import ComponentSetup
from ..vendor import vendor_descriptor


@auto_str
class KostalPikoOldConfiguration:
    def __init__(self, url: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None):
        self.url = url
        self.user = user
        self.password = password


@auto_str
class KostalPikoOld:
    def __init__(self,
                 name: str = "Kostal Piko (alte Generation)",
                 type: str = "kostal_piko_old",
                 id: int = 0,
                 configuration: KostalPikoOldConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.vendor = vendor_descriptor.configuration_factory().type
        self.id = id
        self.configuration = configuration or KostalPikoOldConfiguration()


@auto_str
class KostalPikoOldInverterConfiguration:
    def __init__(self):
        pass


@auto_str
class KostalPikoOldInverterSetup(ComponentSetup[KostalPikoOldInverterConfiguration]):
    def __init__(self,
                 name: str = "Kostal Piko (alte Generation) Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: KostalPikoOldInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or KostalPikoOldInverterConfiguration())
