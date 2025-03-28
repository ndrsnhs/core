#!/usr/bin/env python3
from typing import Dict, Union
from modules.common.abstract_device import AbstractCounter
from modules.common.fault_state import ComponentInfo, FaultState

from dataclass_utils import dataclass_from_dict
from modules.common.component_type import ComponentDescriptor
from modules.devices.generic.mqtt.config import MqttCounterSetup


class MqttCounter(AbstractCounter):
    def __init__(self, component_config: Union[Dict, MqttCounterSetup]) -> None:
        self.component_config = dataclass_from_dict(MqttCounterSetup, component_config)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))


component_descriptor = ComponentDescriptor(configuration_factory=MqttCounterSetup)
