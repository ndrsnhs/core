from unittest.mock import MagicMock, Mock

import pytest

from control.bat import Set
from modules.common.modbus import ModbusDataType
from modules.devices.elmi.elmi.bat import ElmiBat
from modules.devices.elmi.elmi.config import ElmiBatSetup, ElmiCounterSetup, ElmiInverterSetup
from modules.devices.elmi.elmi.counter import ElmiCounter
from modules.devices.elmi.elmi.inverter import ElmiInverter


@pytest.fixture
def client():
    client = MagicMock()
    client.write_register.return_value.isError.return_value = False
    client.read_holding_registers.side_effect = lambda register, *args, **kwargs: {
        1024: 20000, 1046: 1, 1052: 0xFFFFFFFF, 1004: 7650,
        1074: [1000000, 2000000], 1054: [0, 1],
        1070: [0, -123450], 1030: [100, 200, 300],
        1036: [23000, 23100, 23200], 1042: 50000, 1068: 45670,
    }[register]
    return client


def prepare(component):
    component.client = component.kwargs['client']
    component.store = Mock()
    component.peak_filter = Mock()
    component.sim_counter = Mock()
    component.sim_counter.sim_count.return_value = (123, 456)
    return component


@pytest.fixture
def bat(client):
    bat = prepare(ElmiBat(ElmiBatSetup(), client=client, device_id=0))
    bat.last_setpoint_write = None
    return bat


@pytest.mark.parametrize("requested,evu,expected", [
    (10000, 8000, 160000), (-10000, 8000, -40000),
    (0, 8000, 60000), (0, -8000, -100000), (5000, -3000, 0),
])
def test_grid_setpoint_and_heartbeat(bat, client, requested, evu, expected):
    bat.set_power_limit(Set(power_limit=requested, evu_power=evu))
    assert client.write_register.call_args_list[0].args == (1204, 0)
    client.write_register.assert_called_with(1200, expected, data_type=ModbusDataType.INT_32, unit=1)


@pytest.mark.parametrize("requested,evu", [(None, 2000), (10000, None), (0, None)])
def test_release_or_missing_meter_does_not_renew_heartbeat(bat, client, requested, evu):
    bat.set_power_limit(Set(power_limit=requested, evu_power=evu))
    client.write_register.assert_not_called()


def test_rate_limit_does_not_suppress_heartbeat(bat, client, monkeypatch):
    clock = Mock(return_value=0)
    monkeypatch.setattr("modules.devices.elmi.elmi.bat.time.monotonic", clock)
    bat.set_power_limit(Set(power_limit=10000, evu_power=8000))
    client.write_register.reset_mock()
    clock.return_value = 10
    bat.set_power_limit(Set(power_limit=0, evu_power=8000))
    assert [call.args[0] for call in client.write_register.call_args_list] == [1204]
    client.write_register.reset_mock()
    clock.return_value = 11
    bat.set_power_limit(Set(power_limit=0, evu_power=8000))
    assert [call.args[0] for call in client.write_register.call_args_list] == [1204, 1200]


def test_discharge_power_sign(bat, client):
    client.read_holding_registers.side_effect = lambda reg, *args, **kwargs: {
        1024: 20000, 1046: 2, 1052: 5,
    }[reg]
    bat.set_power_limit(Set(power_limit=10000, evu_power=8000))
    client.write_register.assert_called_with(1200, 200000, data_type=ModbusDataType.INT_32, unit=1)


def test_measurements(bat, client, mock_pub):
    bat.update()
    state = bat.store.set.call_args.args[0]
    assert (state.power, state.soc, state.imported, state.exported) == (2000, 76.5, 123, 456)
    mock_pub.pub.assert_any_call("openWB/set/bat/0/get/max_charge_power", 100000)
    mock_pub.pub.assert_any_call("openWB/set/bat/0/get/max_discharge_power", 0)
    counter = prepare(ElmiCounter(ElmiCounterSetup(), client=client, device_id=0))
    counter.update()
    state = counter.store.set.call_args.args[0]
    assert state.power == -12345
    assert state.currents == [-1, -2, -3]
    assert state.voltages == [230, 231, 232]
    assert state.frequency == 50
    inverter = prepare(ElmiInverter(ElmiInverterSetup(), client=client, device_id=0))
    inverter.update()
    assert inverter.store.set.call_args.args[0].power == -4567


def test_rejected_heartbeat_prevents_setpoint(bat, client):
    client.write_register.return_value.isError.return_value = True
    with pytest.raises(RuntimeError, match="1204"):
        bat.set_power_limit(Set(power_limit=10000, evu_power=8000))
    assert [call.args[0] for call in client.write_register.call_args_list] == [1204]
    assert bat.last_setpoint_write is None


def test_rejected_setpoint_is_retried(bat, client):
    def reject_setpoint(address, *args, **kwargs):
        return Mock(isError=Mock(return_value=address == 1200))
    client.write_register.side_effect = reject_setpoint
    with pytest.raises(RuntimeError, match="1200"):
        bat.set_power_limit(Set(power_limit=10000, evu_power=8000))
    assert bat.last_setpoint_write is None
    client.write_register.side_effect = None
    bat.set_power_limit(Set(power_limit=10000, evu_power=8000))
    assert bat.last_setpoint_write is not None


def test_out_of_range_does_not_renew_heartbeat(bat, client):
    with pytest.raises(ValueError):
        bat.set_power_limit(Set(power_limit=2 ** 31, evu_power=8000))
    client.write_register.assert_not_called()
