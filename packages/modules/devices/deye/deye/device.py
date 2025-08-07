#!/usr/bin/env python3
import logging
from typing import Iterable, Optional, List, Union
from contextlib import closing
from pysolarmanv5 import PySolarmanV5

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, MultiComponentUpdater
from modules.common.modbus import ModbusDataType, ModbusTcpClient_
from modules.devices.deye.deye.bat import DeyeBat
from modules.devices.deye.deye.counter import DeyeCounter
from modules.devices.deye.deye.inverter import DeyeInverter
from modules.devices.deye.deye import bat, counter, inverter
from modules.devices.deye.deye.config import Deye, DeyeBatSetup, DeyeConfiguration, DeyeCounterSetup, DeyeInverterSetup
from modules.devices.deye.deye.device_type import DeviceType

log = logging.getLogger(__name__)


def create_device(device_config: Deye):
    client = None
    device_type = None

    def create_bat_component(component_config: DeyeBatSetup):
        nonlocal client
        return DeyeBat(component_config=component_config,
                       device_id=device_config.id,
                       modbus_id=device_config.configuration.modbus_id,
                       client=client,
                       device_type=device_type)

    def create_counter_component(component_config: DeyeCounterSetup):
        nonlocal client
        return DeyeCounter(component_config=component_config,
                           device_id=device_config.id,
                           modbus_id=device_config.configuration.modbus_id,
                           client=client,
                           device_type=device_type)

    def create_inverter_component(component_config: DeyeInverterSetup):
        nonlocal client
        return DeyeInverter(component_config=component_config,
                            device_id=device_config.id,
                            modbus_id=device_config.configuration.modbus_id,
                            client=client,
                            device_type=device_type)

    def update_components(components: Iterable[Union[DeyeBat, DeyeCounter, DeyeInverter]]):
        nonlocal client
        if device_config.configuration.lsw:
            with closing(client):
                for component in components:
                    with SingleComponentUpdateContext(component.fault_state):
                        component.update()
        else:
            with client:
                for component in components:
                    with SingleComponentUpdateContext(component.fault_state):
                        component.update()

    def initializer():
        nonlocal client, device_type
        if device_config.configuration.lsw:
            client = PySolarmanV5(device_config.configuration.ip_address,
                                  device_config.configuration.serial,
                                  port=device_config.configuration.port,
                                  mb_slave_id=device_config.configuration.modbus_id,
                                  auto_reconnect=True,
                                  socket_timeout=15)
            device_type = DeviceType(client.read_holding_registers(0, 1))
        else:
            client = ModbusTcpClient_(device_config.configuration.ip_address, device_config.configuration.port)
            device_type = DeviceType(client.read_holding_registers(
                0, ModbusDataType.INT_16, unit=device_config.configuration.modbus_id))

    return ConfigurableDevice(
        device_config=device_config,
        initializer=initializer,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component,
            counter=create_counter_component,
            inverter=create_inverter_component,
        ),
        component_updater=MultiComponentUpdater(update_components)
    )


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "counter": counter,
    "inverter": inverter
}


def read_legacy(component_type: str, ip_address: str, port: int, modbus_id: int, num: Optional[int] = None) -> None:
    device_config = Deye(configuration=DeyeConfiguration(
        port=port, ip_address=ip_address))

    dev = create_device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config.configuration.modbus_id = modbus_id
    component_config.id = num
    dev.add_component(component_config)

    log.debug('Deye Port: ' + str(port))
    log.debug('Deye ID: ' + str(modbus_id))
    log.debug('Deye IP-Adresse: ' + ip_address)

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Deye)
