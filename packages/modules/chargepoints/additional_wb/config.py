from typing import Optional

from modules.common.abstract_chargepoint import SetupChargepoint


class AdditionalWBConfiguration:
    def __init__(self,
                 ip_address: Optional[str] = None,
                 token: Optional[str] = None):
        self.ip_address = ip_address
        self.token = token


class AdditionalWB(SetupChargepoint[AdditionalWBConfiguration]):
    def __init__(self,
                 name: str = "Additional WB",
                 type: str = "additional_wb",
                 id: int = 0,
                 configuration: AdditionalWBConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or AdditionalWBConfiguration())
