import logging
from typing import TypedDict, Any, Union, Optional
from pysolarmanv5 import PySolarmanV5
from modules.common.abstract_device import AbstractBat
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType, ModbusTcpClient_
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.deye.deye.config import DeyeBatSetup
from modules.devices.deye.deye.device_type import DeviceType

log = logging.getLogger(__name__)


class KwargsDict(TypedDict):
    device_id: int
    modbus_id: int
    client: Union[ModbusTcpClient_, PySolarmanV5]
    device_type: DeviceType


class DeyeBat(AbstractBat):
    def __init__(self, component_config: DeyeBatSetup, **kwargs: Any) -> None:
        self.component_config = component_config
        self.kwargs: KwargsDict = kwargs

    def initialize(self) -> None:
        self.__device_id: int = self.kwargs['device_id']
        self.modbus_id: int = self.kwargs['modbus_id']
        self.client: Union[ModbusTcpClient_, PySolarmanV5] = self.kwargs['client']
        self.device_type = self.kwargs['device_type']
        self.store = get_bat_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")

    def update(self) -> None:
        if self.device_type == DeviceType.SINGLE_PHASE_STRING or self.device_type == DeviceType.SINGLE_PHASE_HYBRID:
            power = self.read_registers(reg=190, length=1, modbus_type=ModbusDataType.INT_16, unit=self.modbus_id) * -1
            soc = self.read_registers(reg=184, length=1, modbus_type=ModbusDataType.INT_16, unit=self.modbus_id)

            if self.device_type == DeviceType.SINGLE_PHASE_HYBRID:
                imported = self.read_registers(
                    reg=72, length=1, modbus_type=ModbusDataType.UINT_16, unit=self.modbus_id) * 100
                exported = self.read_registers(
                    reg=74, length=1, modbus_type=ModbusDataType.UINT_16, unit=self.modbus_id) * 100

            elif self.device_type == DeviceType.SINGLE_PHASE_STRING:
                imported, exported = self.sim_counter.sim_count(power)

        else:  # THREE_PHASE_LV (0x0500, 0x0005), THREE_PHASE_HV (0x0006)
            power = self.read_registers(reg=590, length=1, modbus_type=ModbusDataType.INT_16, unit=self.modbus_id) * -1

            if self.device_type == DeviceType.THREE_PHASE_HV:
                power = power * 10
            soc = self.read_registers(reg=588, length=1, modbus_type=ModbusDataType.INT_16, unit=self.modbus_id)
            imported, exported = self.sim_counter.sim_count(power)

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)

    def read_registers(self,
                       reg: int,
                       length: int = 1,
                       modbus_type: Optional[ModbusDataType] = None,
                       unit: Optional[int] = None) -> int:
        if isinstance(self.client, ModbusTcpClient_):
            return self.client.read_holding_registers(reg, [modbus_type]*length, unit=unit)
        else:
            return self.client.read_holding_registers(reg, length)


component_descriptor = ComponentDescriptor(configuration_factory=DeyeBatSetup)
