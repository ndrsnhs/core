#!/usr/bin/env python3
from typing import TypedDict, Any

from modules.common.abstract_device import AbstractCounter
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_component_value_store
from modules.common.utils.peak_filter import PeakFilter
from modules.devices.sofar.sofar_solarman.config import SofarSolarmanCounterSetup
from modules.common.component_type import ComponentType
from pysolarmanv5 import PySolarmanV5 as ModbusSolarmanClient_


class KwargsDict(TypedDict):
    device_id: int
    client: ModbusSolarmanClient_


class SofarSolarmanCounter(AbstractCounter):
    def __init__(self, component_config: SofarSolarmanCounterSetup, **kwargs: Any) -> None:
        self.component_config = component_config
        self.kwargs: KwargsDict = kwargs

    def initialize(self) -> None:
        self.__device_id: int = self.kwargs['device_id']
        self.client: ModbusSolarmanClient_ = self.kwargs['client']
        self.store = get_component_value_store(self.component_config.type, self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.peak_filter = PeakFilter(ComponentType.COUNTER, self.component_config.id, self.fault_state)

    def update(self):
        power = self.client.read_holding_registers(0x0488, 1)[0] * -10
        frequency = self.client.read_holding_registers(0x0484, 1)[0] / 100
        try:
            powers = [
                self.client.read_holding_registers(0x0493, 1)[0] * -10,
                self.client.read_holding_registers(0x049E, 1)[0] * -10,
                self.client.read_holding_registers(0x04A9, 1)[0] * -10]
        except Exception:
            powers = None
        exported = self.client.read_holding_registers(0x0692, 1)[0] * 100
        imported = self.client.read_holding_registers(0x068E, 1)[0] * 100

        imported, exported = self.peak_filter.check_values(power, imported, exported)
        counter_state = CounterState(
            powers=powers,
            power=power,
            imported=imported,
            exported=exported,
            frequency=frequency
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SofarSolarmanCounterSetup)
