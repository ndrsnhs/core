#!/usr/bin/env python3
import logging
from typing import TypedDict, Any, Optional

from modules.common import modbus
from modules.common.abstract_device import AbstractBat
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.saxpower.saxpower.config import SaxpowerBatSetup

log = logging.getLogger(__name__)


class KwargsDict(TypedDict):
    device_id: int
    client: modbus.ModbusTcpClient_
    modbus_id: int


class SaxpowerBat(AbstractBat):
    def __init__(self, component_config: SaxpowerBatSetup, **kwargs: Any) -> None:
        self.component_config = component_config
        self.kwargs: KwargsDict = kwargs

    def initialize(self) -> None:
        self.__device_id: int = self.kwargs['device_id']
        self.__tcp_client: modbus.ModbusTcpClient_ = self.kwargs['client']
        self.__modbus_id: int = self.kwargs['modbus_id']
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.last_mode = 'Undefined'

    def update(self) -> None:
        with self.__tcp_client:
            # Die beiden Register müssen zwingend zusammen ausgelesen werden, sonst scheitert die zweite Abfrage.
            soc, power = self.__tcp_client.read_holding_registers(46, [ModbusDataType.INT_16]*2, unit=self.__modbus_id)
            power = power * -1 + 16384

        imported, exported = self.sim_counter.sim_count(power)
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)

    def set_power_limit(self, power_limit: Optional[int]) -> None:
        unit = self.device_config.configuration.modbus_id
        log.debug(f'last_mode: {self.last_mode}')

        if power_limit is None:
            # Bei Saxpower muss der Smartmeter in gesonderter Software aktiviert/ deaktiviert werden.
            log.debug("Bei Saxpower muss der Smartmeter in gesonderter Software aktiviert/ deaktiviert werden.")
            if self.last_mode is not None:
                self.last_mode = None
        elif power_limit == 0:
            log.debug("Aktive Batteriesteuerung. Batterie wird auf Stop gesetzt und nicht entladen")
            if self.last_mode != 'stop':
                self.__tcp_client.write_registers(0x29, 0, data_type=ModbusDataType.INT_16, unit=unit)
                self.last_mode = 'stop'
        elif power_limit > 0:
            log.debug(f"Aktive Batteriesteuerung. Batterie wird mit {power_limit} W entladen für den Hausverbrauch")
            if self.last_mode != 'discharge':
                self.last_mode = 'discharge'
            # Die maximale Entladeleistung begrenzen auf 4600W, maximaler Wertebereich Saxpower.
            power_value = int(min(abs(power_limit), 4600))
            log.debug(f"Aktive Batteriesteuerung. Batterie wird mit {power_value} W entladen für den Hausverbrauch")
            self.__tcp_client.write_registers(0x29, [power_value], data_type=ModbusDataType.INT_16, unit=unit)

    def power_limit_controllable(self) -> bool:
        return True


component_descriptor = ComponentDescriptor(configuration_factory=SaxpowerBatSetup)
