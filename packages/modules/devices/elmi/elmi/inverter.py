from modules.common.abstract_device import AbstractInverter
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor, ComponentType
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_component_value_store
from modules.common.utils.peak_filter import PeakFilter
from modules.devices.elmi.elmi.config import ElmiInverterSetup


class ElmiInverter(AbstractInverter):
    def __init__(self, component_config: ElmiInverterSetup, **kwargs):
        self.component_config = component_config
        self.kwargs = kwargs

    def initialize(self):
        self.client = self.kwargs['client']
        self.store = get_component_value_store(self.component_config.type, self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.peak_filter = PeakFilter(ComponentType.INVERTER, self.component_config.id, self.fault_state)
        self.sim_counter = SimCounter(self.kwargs['device_id'], self.component_config.id, self.component_config.type)

    def update(self):
        power = -self.client.read_holding_registers(
            1068, ModbusDataType.UINT_32, unit=self.component_config.configuration.modbus_id) / 10
        self.peak_filter.check_values(power)
        imported, exported = self.sim_counter.sim_count(power)
        self.store.set(InverterState(power=power, imported=imported, exported=exported))


component_descriptor = ComponentDescriptor(configuration_factory=ElmiInverterSetup)
