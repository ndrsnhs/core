#!/usr/bin/env python3
from typing import TypedDict, Any

from modules.common import modbus
from modules.common.abstract_device import AbstractBat
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType
from modules.common.store import get_bat_value_store
from modules.devices.siemens.siemens_sentron.config import SiemensSentronBatSetup


class KwargsDict(TypedDict):
    client: modbus.ModbusTcpClient_
    modbus_id: int


class SiemensSentronBat(AbstractBat):
    def __init__(self, component_config: SiemensSentronBatSetup, **kwargs: Any) -> None:
        self.component_config = component_config
        self.kwargs: KwargsDict = kwargs

    def initialize(self) -> None:
        self.__tcp_client: modbus.ModbusTcpClient_ = self.kwargs['client']
        self.__modbus_id: int = self.kwargs['modbus_id']
        self.store = get_bat_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def update(self) -> None:
        with self.__tcp_client:
            power = self.__tcp_client.read_holding_registers(65, ModbusDataType.FLOAT_32, unit=self.__modbus_id) * -1
            imported = self.__tcp_client.read_holding_registers(801, ModbusDataType.FLOAT_64, unit=self.__modbus_id)
            exported = self.__tcp_client.read_holding_registers(809, ModbusDataType.FLOAT_64, unit=self.__modbus_id)

        bat_state = BatState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=SiemensSentronBatSetup)
