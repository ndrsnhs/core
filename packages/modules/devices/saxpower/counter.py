#!/usr/bin/env python3
from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType, ModbusTcpClient_
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.saxpower.config import SaxpowerCounterSetup


class SaxpowerCounter:
    def __init__(self,
                 device_id: int,
                 component_config: SaxpowerCounterSetup,
                 modbus_id: int) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SaxpowerCounterSetup, component_config)
        self.__modbus_id = modbus_id
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def update(self, client: ModbusTcpClient_):
        power = client.read_holding_registers(48, ModbusDataType.INT_16, unit=self.__modbus_id)
        power = power * -1 + 16384
        imported, exported = self.sim_counter.sim_count(power)

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SaxpowerCounterSetup)
