from dataclasses import dataclass, field
import logging
from typing import List, Optional

from dataclass_utils.factories import currents_list_factory
from helpermodules.constants import NO_ERROR

log = logging.getLogger(__name__)


@dataclass
class Config:
    max_power: float = 0


def config_factory() -> Config:
    return Config()


@dataclass
class Get:
    currents: List[float] = field(default_factory=currents_list_factory, metadata={
                                  "topic": "get/currents"})
    soc: float = field(default=0, metadata={"topic": "get/soc"})
    daily_exported: float = field(default=0, metadata={"topic": "get/daily_exported"})
    daily_imported: float = field(default=0, metadata={"topic": "get/daily_imported"})
    imported: float = field(default=0, metadata={"topic": "get/imported"})
    exported: float = field(default=0, metadata={"topic": "get/exported"})
    fault_state: int = field(default=0, metadata={"topic": "get/fault_state"})
    fault_str: str = field(default=NO_ERROR, metadata={"topic": "get/fault_str"})
    power: float = field(default=0, metadata={"topic": "get/power"})
    power_limit_controllable: bool = field(default=False, metadata={"topic": "get/power_limit_controllable"})
    max_charge_power: float = field(default=0, metadata={"topic": "get/max_charge_power"})
    max_discharge_power: float = field(default=0, metadata={"topic": "get/max_discharge_power"})
    state_str: str = field(default="Keine Steuerung", metadata={"topic": "get/state_str"})


def get_factory() -> Get:
    return Get()


@dataclass
class Set:
    power_limit: Optional[int] = field(default=None, metadata={"topic": "set/power_limit"})


def set_factory() -> Set:
    return Set()


@dataclass
class LimitControllable:
    stop: bool = field(default=False, metadata={"topic": "limit_controllable/stop"})
    charge: bool = field(default=False, metadata={"topic": "limit_controllable/charge"})
    discharge: bool = field(default=False, metadata={"topic": "limit_controllable/discharge"})
    set_power: bool = field(default=False, metadata={"topic": "limit_controllable/set_power"})


def limit_controllable_factory() -> LimitControllable:
    return LimitControllable()


@dataclass
class BatData:
    config: Config = field(default_factory=config_factory)
    get: Get = field(default_factory=get_factory)
    set: Set = field(default_factory=set_factory)
    limit_controllable: LimitControllable = field(default_factory=limit_controllable_factory)


class Bat:

    def __init__(self, index):
        self.data = BatData()
        self.num = index
