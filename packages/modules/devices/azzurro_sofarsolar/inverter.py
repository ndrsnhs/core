#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store
from modules.devices.azzurro_sofarsolar.config import AzzurroInverterSetup

log = logging.getLogger(__name__)


class AzzurroInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, AzzurroInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(AzzurroInverterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def update(self) -> float:
        unit = self.component_config.configuration.modbus_id
        with self.__tcp_client:
            power = self.__tcp_client.read_input_registers(0x0485, ModbusDataType.INT_16, unit=unit) * -1000

            exported = self.__tcp_client.read_holding_registers(
                0x0687, ModbusDataType.UINT_32, unit=unit) * 100
        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.store.set(inverter_state)
        return power


component_descriptor = ComponentDescriptor(configuration_factory=AzzurroInverterSetup)
