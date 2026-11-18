from typing import Iterable, Union

from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.configurable_device import ComponentFactoryByType, ConfigurableDevice, MultiComponentUpdater
from modules.common.modbus import ModbusTcpClient_
from modules.devices.elmi.elmi.bat import ElmiBat
from modules.devices.elmi.elmi.config import Elmi, ElmiBatSetup, ElmiCounterSetup, ElmiInverterSetup
from modules.devices.elmi.elmi.counter import ElmiCounter
from modules.devices.elmi.elmi.inverter import ElmiInverter


def create_device(device_config: Elmi):
    client = None

    def create_bat_component(component_config: ElmiBatSetup):
        return ElmiBat(component_config, device_id=device_config.id, client=client)

    def create_counter_component(component_config: ElmiCounterSetup):
        return ElmiCounter(component_config, device_id=device_config.id, client=client)

    def create_inverter_component(component_config: ElmiInverterSetup):
        return ElmiInverter(component_config, device_id=device_config.id, client=client)

    def update_components(components: Iterable[Union[ElmiBat, ElmiCounter, ElmiInverter]]):
        with client:
            for component in components:
                with SingleComponentUpdateContext(component.fault_state):
                    component.update()

    def initializer():
        nonlocal client
        client = ModbusTcpClient_(device_config.configuration.ip_address, device_config.configuration.port,
                                  timeout=1)

    return ConfigurableDevice(
        device_config=device_config,
        initializer=initializer,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component, counter=create_counter_component, inverter=create_inverter_component),
        component_updater=MultiComponentUpdater(update_components)
    )


device_descriptor = DeviceDescriptor(
    configuration_factory=Elmi,
    compatibility_bat_note="ModbusTCP V2.2: Grid-Sollwert alle >10 s, Heartbeat innerhalb 30 s. "
    "ELMI nennt mindestens +5 kW / -10 kW. Interner EMS-Plan bleibt aktiv; "
    "ForceSOC_StartChg und End SOC beachten. Freigabe erfolgt über die Offline-Strategie.")
