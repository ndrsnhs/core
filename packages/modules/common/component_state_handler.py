import logging
from control import data
from typing import Optional, Union, List
from modules.common.simcount import SimCounter
from modules.common.component_state import CounterState, InverterState, BatState
# from control import data


log = logging.getLogger(__name__)


class ComponentStateHandler:
    def __init__(self, type: str, device_id: int, component_id: int, use_sim_counter: Optional[bool] = False):
        self.type = type
        self.device_id = device_id
        self.component_id = component_id
        self.sim_counter = self.init_sim_counter(device_id, component_id) if use_sim_counter else None

    def init_sim_counter(self, device_id: int, component_id: int) -> SimCounter:
        if self.type == "counter":
            return SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        elif self.type == "inverter":
            return SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        elif self.type == "bat":
            return SimCounter(self.__device_id, self.component_config.id, prefix="speicher")

    def update(
        self,
        power: float,
        imported: Optional[float],
        exported: Optional[float],
        voltages: Optional[List[Optional[float]]],
        currents: Optional[List[Optional[float]]],
        powers: Optional[List[Optional[float]]],
        power_factors: Optional[List[Optional[float]]],
        frequency: Optional[float],
        serial_number: Optional[str],
        dc_power: Optional[float],
        soc: Optional[float]
    ) -> Union[CounterState, InverterState, BatState]:
        self.check_values(power, imported, exported)
        if self.sim_counter is not None:
            imported, exported = self.sim_counter.sim_count(power)
        if self.type == "counter":
            return CounterState(
                power=power,
                imported=imported,
                exported=exported,
                voltages=voltages,
                currents=currents,
                powers=powers,
                power_factors=power_factors,
                frequency=frequency,
                serial_number=serial_number
            )
        elif self.type == "inverter":
            return InverterState(
                power=power,
                exported=exported,
                imported=imported,
                currents=currents,
                dc_power=dc_power,
                serial_number=serial_number,
            )
        elif self.type == "bat":
            return BatState(
                power=power,
                imported=imported,
                exported=exported,
                soc=soc,
                currents=currents,
                serial_number=serial_number,
            )

    def check_values(
        self,
        power: float,
        imported: Optional[float] = None,
        exported: Optional[float] = None
    ) -> None:
        if self.type == "inverter":
            inverter = data.data.pv_data[f"pv{self.component_id}"]
            max_ac_out = inverter.data.config.max_ac_out
            if max_ac_out > 0 and power > 2 * max_ac_out:
                raise Exception("Leistung überschreitet max. AC-Ausgangsleistung des Wechselrichters")
        elif self.type == "counter":
            counter = data.data.counter_data[f"counter{self.component_id}"]
            max_total_power = counter.data.config.max_total_power
            if abs(power) > 2 * max_total_power:
                raise Exception("Leistung überschreitet max. Gesamtleistung des Zählers")

        # bat_handling
        # bat = data.data.bat_data[f"bat{self.component_id}"]

        # maximale Leistung in W mit Zeiteinheit umrechnen in Wattstunden
        # mit vorherigen Zählerstand vergleichen.
        # Was passiert wenn verworfen wird. -> mit Timestamps arbeiten?
