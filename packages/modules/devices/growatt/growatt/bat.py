#!/usr/bin/env python3
import logging
from typing import TypedDict, Any, Optional

from modules.common.abstract_device import AbstractBat
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType, ModbusTcpClient_
from modules.common.store import get_bat_value_store
from modules.devices.growatt.growatt.config import GrowattBatSetup
from modules.devices.growatt.growatt.version import GrowattVersion

log = logging.getLogger(__name__)


class KwargsDict(TypedDict):
    modbus_id: int
    version: GrowattVersion
    client: ModbusTcpClient_


class GrowattBat(AbstractBat):
    def __init__(self, component_config: GrowattBatSetup, **kwargs: Any) -> None:
        self.component_config = component_config
        self.kwargs: KwargsDict = kwargs

    def initialize(self) -> None:
        self.__modbus_id: int = self.kwargs['modbus_id']
        self.version: GrowattVersion = self.kwargs['version']
        self.client: ModbusTcpClient_ = self.kwargs['client']
        self.store = get_bat_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def update(self) -> None:
        if self.version == GrowattVersion.max_series:
            power_in = self.client.read_input_registers(
                1011, ModbusDataType.UINT_32, unit=self.__modbus_id) * 0.1
            power_out = self.client.read_input_registers(
                1009, ModbusDataType.UINT_32, unit=self.__modbus_id) * -0.1
            power = power_in + power_out

            soc = self.client.read_input_registers(1014, ModbusDataType.UINT_16, unit=self.__modbus_id)
            imported = self.client.read_input_registers(
                1058, ModbusDataType.UINT_32, unit=self.__modbus_id) * 100
            exported = self.client.read_input_registers(
                1054, ModbusDataType.UINT_32, unit=self.__modbus_id) * 100
        else:
            power_in = self.client.read_input_registers(
                3180, ModbusDataType.UINT_32, unit=self.__modbus_id) * -0.1
            power_out = self.client.read_input_registers(
                3178, ModbusDataType.UINT_32, unit=self.__modbus_id) * 0.1
            power = power_in + power_out

            soc = self.client.read_input_registers(3171, ModbusDataType.UINT_16, unit=self.__modbus_id)
            imported = self.client.read_input_registers(
                3131, ModbusDataType.UINT_32, unit=self.__modbus_id) * 100
            exported = self.client.read_input_registers(
                3127, ModbusDataType.UINT_32, unit=self.__modbus_id) * 100

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)

    def set_power_limit(self, power_limit: Optional[int]) -> None:
        unit = self.__modbus_id
        if self.version == GrowattVersion.max_series:
            log.debug(f'last_mode: {self.last_mode}')

            if power_limit is None:
                log.debug("Keine Batteriesteuerung, Selbstregelung durch Wechselrichter")
                if self.last_mode is not None:
                    # disable battery first
                    self.__tcp_client.write_registers(1102, [0], data_type=ModbusDataType.UINT_16, unit=unit)
                    # disable ac_charge
                    self.__tcp_client.write_registers(1092, [0], data_type=ModbusDataType.UINT_16, unit=unit)
                    self.last_mode = None
            elif power_limit <= 0:
                log.debug("Aktive Batteriesteuerung. Batterie wird auf Stop gesetzt und nicht entladen")
                if self.last_mode != 'stop':
                    # enable battery first
                    self.__tcp_client.write_registers(1102, [1], data_type=ModbusDataType.UINT_16, unit=unit)
                    # disable ac_charge
                    self.__tcp_client.write_registers(1092, [0], data_type=ModbusDataType.UINT_16, unit=unit)
                    self.last_mode = 'stop'
            else:
                log.debug("Aktive Batteriesteuerung. Batterie wird geladen")
                if self.last_mode != 'charge':
                    # enable battery first
                    self.__tcp_client.write_registers(1102, [1], data_type=ModbusDataType.UINT_16, unit=unit)
                    # enable ac_charge
                    self.__tcp_client.write_registers(1092, [1], data_type=ModbusDataType.UINT_16, unit=unit)
                    self.last_mode = 'charge'

    def power_limit_controllable(self) -> bool:
        if self.version == GrowattVersion.max_series:
            return True
        else:
            return False


component_descriptor = ComponentDescriptor(configuration_factory=GrowattBatSetup)
