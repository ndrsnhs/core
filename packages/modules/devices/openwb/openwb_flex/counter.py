#!/usr/bin/env python3
from typing import TypedDict, Any

from modules.common import modbus
from modules.common.abstract_device import AbstractCounter
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.lovato import Lovato
from modules.common.mpm3pm import Mpm3pm
from modules.common.b23 import B23
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.openwb.openwb_flex.config import EvuKitFlexSetup
from modules.devices.openwb.openwb_flex.versions import kit_counter_version_factory


class KwargsDict(TypedDict):
    device_id: int
    client: modbus.ModbusTcpClient_


class EvuKitFlex(AbstractCounter):
    def __init__(self, component_config: EvuKitFlexSetup, **kwargs: Any) -> None:
        self.component_config = component_config
        self.kwargs: KwargsDict = kwargs

    def initialize(self) -> None:
        self.__device_id: int = self.kwargs['device_id']
        self.__tcp_client: modbus.ModbusTcpClient_ = self.kwargs['client']
        factory = kit_counter_version_factory(self.component_config.configuration.version)
        self.__client = factory(self.component_config.configuration.id, self.__tcp_client)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def update(self):
        # TCP-Verbindung schließen möglichst bevor etwas anderes gemacht wird, um im Fehlerfall zu verhindern,
        # dass offene Verbindungen den Modbus-Adapter blockieren.
        with self.__tcp_client:
            voltages = self.__client.get_voltages()
            powers, power = self.__client.get_power()
            frequency = self.__client.get_frequency()
            power_factors = self.__client.get_power_factors()

            if isinstance(self.__client, Mpm3pm or B23):
                imported = self.__client.get_imported()
                exported = self.__client.get_exported()
            else:
                currents = self.__client.get_currents()

        if isinstance(self.__client, Mpm3pm or B23):
            currents = [powers[i] / voltages[i] for i in range(3)]
        else:
            if isinstance(self.__client, Lovato):
                power = sum(powers)
            imported, exported = self.sim_counter.sim_count(power)
        counter_state = CounterState(
            voltages=voltages,
            currents=currents,
            powers=powers,
            power_factors=power_factors,
            imported=imported,
            exported=exported,
            power=power,
            frequency=frequency
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=EvuKitFlexSetup)
