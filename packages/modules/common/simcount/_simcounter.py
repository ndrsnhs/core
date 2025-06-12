from typing import Tuple, Optional


from control import data
from modules.common.simcount._simcount import sim_count
from modules.common.simcount.simcounter_state import SimCounterState


class SimCounter:
    def __init__(self, device_id: int, component_id: int, prefix: str):
        self.topic = "openWB/set/system/device/{}/component/{}/".format(device_id, component_id)
        self.prefix = "pv2" if prefix == "pv" and component_id != 1 else prefix
        self.data: Optional[SimCounterState] = None
        self.component_id = component_id

    def sim_count(self, power: float) -> Tuple[float, float]:
        if self.prefix == "pv" or self.prefix == "pv2":
            inverter = data.data.pv_data[f"pv{self.delegate.delegate.num}"]
            max_ac_out = inverter.data.config.max_ac_out
            if max_ac_out > 0 and power > 2 * max_ac_out:
                raise Exception("Leistung überschreitet max. AC-Ausgangsleistung des Wechselrichters")
        self.data = sim_count(power, self.topic, self.data, self.prefix)
        return self.data.imported, self.data.exported


class SimCounterChargepoint:
    def __init__(self, chargepoint_id: int):
        self.topic = f"openWB/set/chargepoint/{chargepoint_id}/get/"
        self.data = None  # type: Optional[SimCounterState]

    def sim_count(self, power: float) -> Tuple[float, float]:
        self.data = sim_count(power, self.topic, self.data, "")
        return self.data.imported, self.data.exported
