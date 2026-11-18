from modules.common.abstract_device import AbstractCounter
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor, ComponentType
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_component_value_store
from modules.common.utils.peak_filter import PeakFilter
from modules.devices.elmi.elmi.config import ElmiCounterSetup


class ElmiCounter(AbstractCounter):
    def __init__(self, component_config: ElmiCounterSetup, **kwargs):
        self.component_config = component_config
        self.kwargs = kwargs

    def initialize(self):
        self.client = self.kwargs['client']
        self.store = get_component_value_store(self.component_config.type, self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.peak_filter = PeakFilter(ComponentType.COUNTER, self.component_config.id, self.fault_state)
        self.sim_counter = SimCounter(self.kwargs['device_id'], self.component_config.id, self.component_config.type)

    def update(self):
        unit = self.component_config.configuration.modbus_id
        imported_power, exported_power = self.client.read_holding_registers(
            1070, [ModbusDataType.UINT_32, ModbusDataType.INT_32], unit=unit)
        power = (imported_power + exported_power) / 10
        currents = [value / 100 for value in self.client.read_holding_registers(
            1030, [ModbusDataType.UINT_32] * 3, unit=unit)]
        voltages = [value / 100 for value in self.client.read_holding_registers(
            1036, [ModbusDataType.UINT_32] * 3, unit=unit)]
        frequency = self.client.read_holding_registers(1042, ModbusDataType.UINT_32, unit=unit) / 1000
        # Only unsigned phase currents are documented; no phase active powers are available.
        if power < 0:
            currents = [-value for value in currents]
        self.peak_filter.check_values(power)
        imported, exported = self.sim_counter.sim_count(power)
        self.store.set(CounterState(power=power, imported=imported, exported=exported,
                                    currents=currents, voltages=voltages, frequency=frequency))


component_descriptor = ComponentDescriptor(configuration_factory=ElmiCounterSetup)
