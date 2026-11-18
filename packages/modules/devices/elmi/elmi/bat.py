import logging
import time

from helpermodules.pub import Pub
from modules.common.abstract_device import AbstractBat, SetPoint
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor, ComponentType
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_component_value_store
from modules.common.utils.peak_filter import PeakFilter
from modules.devices.elmi.elmi.config import ElmiBatSetup

log = logging.getLogger(__name__)


class ElmiBat(AbstractBat):
    # Strictly greater than 10 seconds, including openWB's fast control cycles.
    SETPOINT_INTERVAL = 11

    def __init__(self, component_config: ElmiBatSetup, **kwargs):
        self.component_config = component_config
        self.kwargs = kwargs

    def initialize(self):
        self.client = self.kwargs['client']
        self.store = get_component_value_store(self.component_config.type, self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.peak_filter = PeakFilter(ComponentType.BAT, self.component_config.id, self.fault_state)
        self.sim_counter = SimCounter(self.kwargs['device_id'], self.component_config.id, self.component_config.type)
        self.last_setpoint_write = None

    def read_power(self):
        unit = self.component_config.configuration.modbus_id
        power = self.client.read_holding_registers(1024, ModbusDataType.INT_32, unit=unit) / 10
        state = self.client.read_holding_registers(1046, ModbusDataType.UINT_32, unit=unit)
        # V2.2 does not specify the sign of 1024. Normalize using the documented state:
        # openWB: charge positive, discharge negative.
        if state == 1:
            return abs(power)
        if state == 2:
            return -abs(power)
        return power

    def update(self):
        unit = self.component_config.configuration.modbus_id
        power = self.read_power()
        soc = self.client.read_holding_registers(
            1004, ModbusDataType.UINT_32, unit=unit) / 100
        charge_power, discharge_power = self.client.read_holding_registers(
            1074, [ModbusDataType.UINT_32] * 2, unit=unit)
        stop_charge, stop_discharge = self.client.read_holding_registers(
            1054, [ModbusDataType.UINT_32] * 2, unit=unit)
        self.peak_filter.check_values(power)
        imported, exported = self.sim_counter.sim_count(power)
        self.store.set(BatState(power=power, soc=soc, imported=imported, exported=exported))
        topic = f"openWB/set/bat/{self.component_config.id}/get/"
        Pub().pub(topic + "max_charge_power", 0 if stop_charge else charge_power / 10)
        Pub().pub(topic + "max_discharge_power", 0 if stop_discharge else discharge_power / 10)

    def set_power_limit(self, setpoint: SetPoint):
        # No release/mode register is documented. Stop renewing the heartbeat to hand
        # control back to ELMI's configured offline strategy (timeout: 30 seconds).
        if setpoint.power_limit is None or setpoint.evu_power is None:
            return
        unit = self.component_config.configuration.modbus_id
        with self.client:
            now = time.monotonic()
            due = self.last_setpoint_write is None or now - self.last_setpoint_write >= self.SETPOINT_INTERVAL
            if due:
                power = self.read_power()
                self.peak_filter.check_values(power)
                grid_setpoint = setpoint.evu_power - power + setpoint.power_limit
                raw_setpoint = round(grid_setpoint * 10)
                if not -(2 ** 31) <= raw_setpoint < 2 ** 31:
                    raise ValueError("ELMI Grid-Sollwert außerhalb des SINT32-Bereichs")
            # Read back and increment, so reconnects/restarts also change the heartbeat.
            heartbeat = self.client.read_holding_registers(1052, ModbusDataType.UINT_32, unit=unit)
            response = self.client.write_register(
                1204, (int(heartbeat) + 1) & 0xFFFFFFFF, data_type=ModbusDataType.UINT_32, unit=unit)
            if response.isError():
                raise RuntimeError(f"ELMI: Schreiben von Register 1204 fehlgeschlagen: {response}")
            if due:
                log.debug("ELMI: EVU %.1f W, Speicher %.1f W, Soll %s W -> Grid-Soll %.1f W",
                          setpoint.evu_power, power, setpoint.power_limit, grid_setpoint)
                response = self.client.write_register(1200, raw_setpoint, data_type=ModbusDataType.INT_32, unit=unit)
                if response.isError():
                    raise RuntimeError(f"ELMI: Schreiben von Register 1200 fehlgeschlagen: {response}")
                self.last_setpoint_write = time.monotonic()

    def power_limit_controllable(self):
        return True


component_descriptor = ComponentDescriptor(configuration_factory=ElmiBatSetup)
