#!/usr/bin/env python3
import logging
from requests import HTTPError

from modules.common.abstract_device import AbstractCounter
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_counter_value_store
from modules.devices.tesla.tesla.config import TeslaCounterSetup
from modules.devices.tesla.tesla.http_client import PowerwallHttpClient

log = logging.getLogger(__name__)


class TeslaCounter(AbstractCounter):
    def __init__(self, component_config: TeslaCounterSetup) -> None:
        self.component_config = component_config

    def initialize(self) -> None:
        self.store = get_counter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def update(self, client: PowerwallHttpClient, aggregate):
        # read firmware version
        status = client.get_json("/api/status")
        log.debug('Firmware: ' + status["version"])
        try:
            # read additional info if firmware supports
            meters_site = client.get_json("/api/meters/site")
            powerwall_state = CounterState(
                imported=aggregate["site"]["energy_imported"],
                exported=aggregate["site"]["energy_exported"],
                power=aggregate["site"]["instant_power"],
                voltages=[meters_site[0]["Cached_readings"]["v_l" + str(phase) + "n"] for phase in range(1, 4)],
                currents=[meters_site[0]["Cached_readings"]["i_" + phase + "_current"] for phase in ["a", "b", "c"]],
                powers=[meters_site[0]["Cached_readings"]["real_power_" + phase] for phase in ["a", "b", "c"]]
            )
        except (KeyError, HTTPError):
            log.debug(
                "Firmware seems not to provide detailed phase measurements. Fallback to total power only.")
            powerwall_state = CounterState(
                imported=aggregate["site"]["energy_imported"],
                exported=aggregate["site"]["energy_exported"],
                power=aggregate["site"]["instant_power"]
            )
        self.store.set(powerwall_state)


component_descriptor = ComponentDescriptor(configuration_factory=TeslaCounterSetup)
