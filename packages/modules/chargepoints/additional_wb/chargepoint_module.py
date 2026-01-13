
from helpermodules.utils.error_handling import CP_ERROR, ErrorTimerContext
from modules.chargepoints.additional_wb.config import AdditionalWB
from modules.common.abstract_chargepoint import AbstractChargepoint
from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_chargepoint_value_store
from modules.common.component_state import ChargepointState
from modules.common import req


class ChargepointModule(AbstractChargepoint):
    def __init__(self, config: AdditionalWB) -> None:
        self.config = config
        self.store = get_chargepoint_value_store(self.config.id)
        self.fault_state = FaultState(ComponentInfo(
            self.config.id,
            "Ladepunkt", "chargepoint"))
        self.client_error_context = ErrorTimerContext(
            f"openWB/set/chargepoint/{self.config.id}/get/error_timestamp", CP_ERROR, hide_exception=True)
        self.session = req.get_http_session()

    def set_current(self, current: float) -> None:
        if self.client_error_context.error_counter_exceeded():
            current = 0
        with SingleComponentUpdateContext(self.fault_state, update_always=False):
            with self.client_error_context:
                # curl -s -X POST -H "AuthKey: token_here" -d "ampere=12.4" http://<IP>/api/v1/openwb
                self.session.post(f'http://{self.config.configuration.ip_address}/api/v1/openwb',
                                  headers={'AuthKey': self.config.configuration.token},
                                  data={'ampere': current})

    def get_values(self) -> None:
        with SingleComponentUpdateContext(self.fault_state):
            with self.client_error_context:
                # curl -X GET -H "AuthKey: ${openwb_token}" --no-progress-meter -q -s -k http://${host}/api/v1/openwb
                json_rsp = self.session.get(f'http://{self.config.configuration.ip_address}/api/v1/openwb',
                                            headers={"AuthKey": self.config.configuration.token}).json()

                chargepoint_state = ChargepointState(
                    powers=json_rsp["powers"],
                    power=json_rsp["power_all"],
                    currents=json_rsp["currents"],
                    voltages=json_rsp["voltages"],
                    frequency=json_rsp["frequency"],
                    imported=json_rsp["imported"],
                    exported=0,
                    plug_state=json_rsp["plug_state"],
                    charge_state=json_rsp["charge_state"],
                    phases_in_use=json_rsp["phases_in_use"],
                    evse_current=json_rsp["offered_current"],
                    rfid=json_rsp["rfid_tag"],
                    rfid_timestamp=json_rsp["rfid_timestamp"],
                    serial_number=json_rsp["serial_meter"],
                    mid_meter=json_rsp["mid_meter"],
                    max_evse_current=json_rsp["max_current_multi_phases"],
                    version=json_rsp["firmware_version"],
                    # fault_str=json_rsp["fault_str"]
                )

                self.client_error_context.reset_error_counter()
            if self.client_error_context.error_counter_exceeded():
                chargepoint_state = ChargepointState(plug_state=None,
                                                     charge_state=False,
                                                     imported=None,
                                                     exported=None,
                                                     currents=[0]*3,
                                                     phases_in_use=0,
                                                     power=0)
            self.store.set(chargepoint_state)

    def switch_phases(self, phases_to_use: int) -> None:
        with SingleComponentUpdateContext(self.fault_state, update_always=False):
            with self.client_error_context:
                response = self.session.get(f'http://{self.config.configuration.ip_address}/api/v1/openwb',
                                            headers={'AuthKey': self.config.configuration.token})
                if response.json()["phases_target"] != phases_to_use:
                    # curl -s -X POST -H "AuthKey: token_here" -d "phasetarget=3" http://<IP>/api/v1/openwb
                    self.session.post(f'http://{self.config.configuration.ip_address}/api/v1/openwb',
                                      headers={'AuthKey': self.config.configuration.token},
                                      data={'phasetarget': str(1 if phases_to_use == 1 else 3)})

    def clear_rfid(self) -> None:
        pass

    def innterupt_cp(self, duration: int) -> None:
        # curl -s -X POST -H "AuthKey: token_here" -d "cpinterruptduration=5" http://<IP>/api/v1/openwb
        # curl -s -X POST -H "AuthKey: token_here" -d "cpinterrupt=1" http://<IP>/api/v1/openwb

        with SingleComponentUpdateContext(self.fault_state, update_always=False):
            self.session.post(f'http://{self.config.configuration.ip_address}/api/v1/openwb',
                              headers={'AuthKey': self.config.configuration.token},
                              data={'cpinterruptduration': str(duration if duration <= 254 else 254)})
            self.session.post(f'http://{self.config.configuration.ip_address}/api/v1/openwb',
                              headers={'AuthKey': self.config.configuration.token},
                              data={'cpinterrupt': 1})


chargepoint_descriptor = DeviceDescriptor(configuration_factory=AdditionalWB)
