from typing import Dict
from unittest.mock import Mock

import pytest
import requests_mock
from modules.chargepoints.additional_wb.config import AdditionalWB, AdditionalWBConfiguration


from modules.common.component_state import ChargepointState
from modules.chargepoints.additional_wb import chargepoint_module


class Params:
    def __init__(self,
                 name: str,
                 sample_data: Dict,
                 sample_state: ChargepointState):
        self.name = name
        self.sample_data = sample_data
        self.sample_state = sample_state


class TestAdditionalWb:
    SAMPLE_CP_STATE_V1 = ChargepointState(
        powers=[1400, 1400, 1400],
        power=4200,
        currents=[6, 6, 6],
        voltages=[235.05, 234.09, 233.07],
        frequency=49.935,
        imported=17702,
        exported=0,
        plug_state=True,
        charge_state=True,
        phases_in_use=3,
        evse_current=7,
        rfid=None,
        rfid_timestamp=None,
        serial_number='822013',
        max_evse_current=16,
        version='1.2.3',
        # serial_meter=json_rsp["serial_meter"]
        # fault_str=json_rsp["fault_str"]
    )
    SAMPLE_V1 = {
        "timestamp": "2024:12:03-09:14:44",  # local time
        "date": 1733213684,  # unix timestamp
        "powers": [1400, 1400, 1400],  # in Watt, int
        "power_all": 4200,  # total power in Watt
        "currents": [6, 6, 6],  # in Ampere, float
        "voltages": [235.05, 234.09, 233.07],  # in Volt, float
        "frequency": 49.935,  # frequency in Hz
        "imported": 17702,  # meter reading in Wh, int
        "plug_state": True,  # plugged in, bool
        "charge_state": True,  # charging, bool
        "phases_actual": 3,  # available phases for charging, int 0,1,3
        "phases_target": 3,  # configured phase count, int 1,3
        "phases_in_use": 3,  # int 1,2,3, phase is in use if current >= 1A
        "offered_current": 7,   # 0,6-32, float
        "rfid_tag": None,  # RFID tag, int
        "rfid_timestamp": None,  # timestamp of rfid reading
        "serial": "822013",  # serialnumber
        "serial_meter": "1234",  # serialnumber of the meter (currently the same as "serial")
        "firmware_version": "1.2.3",  # Firmware Version of the PNI
        "component_version": "H2 P1 A1.2.3 M22 R6",  # versions of other components
        "mid_meter": True,  # valid meter available, bool
        "fault_state": 0,  # int, 0,1,2 (currently always 0)
        "fault_str": None,  # error message to fault_state, string (currently always null)
        "max_current_single_phase": 20,  # int
        "max_current_multi_phases": 16  # int (currently same as "max_current_single_phase")
    }

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        self.mock_chargepoint_value_store = Mock()
        monkeypatch.setattr(chargepoint_module, 'get_chargepoint_value_store',
                            Mock(return_value=self.mock_chargepoint_value_store))

    @pytest.fixture
    def cp(self) -> chargepoint_module.ChargepointModule:
        return chargepoint_module.ChargepointModule(
            AdditionalWB(configuration=AdditionalWBConfiguration(ip_address="1.1.1.1", token="token"))
        )

    cases = [
        Params("AdditionalWB V1", SAMPLE_V1, SAMPLE_CP_STATE_V1),
    ]

    @pytest.mark.parametrize("params", cases, ids=[c.name for c in cases])
    def test_get_values_v2(self, cp, requests_mock: requests_mock.mock, params: Params):
        # setup
        requests_mock.get("http://1.1.1.1/api/v1/openwb", json=params.sample_data)

        # execution
        cp.get_values()

        # evaluation
        assert self.mock_chargepoint_value_store.set.call_count == 1
        assert vars(self.mock_chargepoint_value_store.set.call_args[0][0]) == vars(params.sample_state)

    def test_set_current(self, cp, requests_mock: requests_mock.Mocker):
        # setup
        requests_mock.get('http://1.1.1.1/api/v1/openwb', json=TestAdditionalWb.SAMPLE_V1)

        # execution
        cp.set_current(14.55)

        # evaluation
        assert requests_mock.request_history[0].text == "ampere=14.55"
