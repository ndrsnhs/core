#!/usr/bin/env python3
from typing import TypedDict, Any

from modules.common.abstract_device import AbstractInverter
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_component_value_store
from modules.common.utils.peak_filter import PeakFilter
from modules.devices.sofar.sofar_solarman.config import SofarSolarmanInverterSetup
from modules.common.component_type import ComponentType
from pysolarmanv5 import PySolarmanV5 as ModbusSolarmanClient_


class KwargsDict(TypedDict):
    device_id: int
    client: ModbusSolarmanClient_


class SofarSolarmanInverter(AbstractInverter):
    def __init__(self, component_config: SofarSolarmanInverterSetup, **kwargs: Any) -> None:
        self.component_config = component_config
        self.kwargs: KwargsDict = kwargs

    def initialize(self) -> None:
        self.__device_id: int = self.kwargs['device_id']
        self.client: ModbusSolarmanClient_ = self.kwargs['client']
        self.store = get_component_value_store(self.component_config.type, self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.peak_filter = PeakFilter(ComponentType.INVERTER, self.component_config.id, self.fault_state)

    def update(self) -> None:
        power = self.client.read_holding_registers(0x05C4, 1)[0] * -100
        exported = self.client.read_holding_registers(0x0686, 1)[0] * 100

        _, exported = self.peak_filter.check_values(power, None, exported)

        inverter_state = InverterState(
            power=power,
            exported=exported,
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SofarSolarmanInverterSetup)
