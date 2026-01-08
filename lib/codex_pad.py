import bluetooth
import struct
import asyncio
import _thread

from micropython import const

TX_POWER_MINUS_16_DBM = const(-16)
TX_POWER_MINUS_12_DBM = const(-12)
TX_POWER_MINUS_8_DBM = const(-8)
TX_POWER_MINUS_5_DBM = const(-5)
TX_POWER_MINUS_3_DBM = const(-3)
TX_POWER_MINUS_1_DBM = const(-0)
TX_POWER_0_DBM = const(0)
TX_POWER_1_DBM = const(1)
TX_POWER_2_DBM = const(2)
TX_POWER_3_DBM = const(3)
TX_POWER_4_DBM = const(4)
TX_POWER_5_DBM = const(5)
TX_POWER_6_DBM = const(6)


_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)
_ADV_SCAN_IND = const(0x02)
_ADV_NONCONN_IND = const(0x03)


_DEVICE_INFO_SERVICE_UUID = bluetooth.UUID(0x180A)
_DEVICE_INFO_MODEL_NUMBER_STRING_UUID = bluetooth.UUID(0x2A24)

_STATE_SERVICE_UUID = bluetooth.UUID(0xFFE0)
_STATE_CHARACTERISTIC_UUID = bluetooth.UUID(0xFF01)
_TX_POWER_CHARACTERISTIC_UUID = bluetooth.UUID(0x2A07)
_CCCD_UUID = bluetooth.UUID(0x2902)


class CodexPad:

    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._event = asyncio.ThreadSafeFlag()
        self._lock = _thread.allocate_lock()
        self._reset()

    def _reset(self):
        self._model_number = None
        self._conn_handle = None
        self._state_value_handle = None
        self._tx_power_value_handle = None
        self._is_connected = False
        self._action_result_data = None
        self._state = None

    def _irq(self, event, data):
        if event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            if self._action_result_data is not None:
                self._action_result_data.append(conn_handle)
            self._event.set()
        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            self._event.set()
            self._reset()
        elif event == _IRQ_GATTC_SERVICE_RESULT:
            if self._action_result_data is not None:
                conn_handle, start_handle, end_handle, uuid = data
                self._action_result_data.append((conn_handle, start_handle, end_handle, bluetooth.UUID(uuid)))
        elif event == _IRQ_GATTC_SERVICE_DONE:
            self._event.set()
        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            if self._action_result_data is not None:
                conn_handle, def_handle, value_handle, properties, uuid = data
                self._action_result_data.append((conn_handle, def_handle, value_handle, properties, bluetooth.UUID(uuid)))
        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            self._event.set()
        elif event == _IRQ_GATTC_DESCRIPTOR_RESULT:
            if self._action_result_data is not None:
                conn_handle, dsc_handle, uuid = data
                self._action_result_data.append((conn_handle, dsc_handle, bluetooth.UUID(uuid)))
        elif event == _IRQ_GATTC_DESCRIPTOR_DONE:
            self._event.set()
        elif event == _IRQ_GATTC_READ_RESULT:
            if self._action_result_data is not None:
                conn_handle, value_handle, char_data = data
                self._action_result_data.append((conn_handle, value_handle, memoryview(char_data)))
        elif event == _IRQ_GATTC_READ_DONE:
            self._event.set()
        elif event == _IRQ_GATTC_WRITE_DONE:
            self._event.set()
        elif event == _IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            if self._state_value_handle == value_handle:
                with self._lock:
                    self._state = bytes(notify_data)

    def connect(self, mac_address):
        result = self._execute_ble_operation(lambda: self._ble.gap_connect(0, bytes.fromhex(mac_address.replace(":", ""))))

        if len(result) != 0:
            self._conn_handle = result[0]
        else:
            raise Exception("Failed to connect")

        services_data = self._execute_ble_operation(lambda: self._ble.gattc_discover_services(self._conn_handle))

        for _, service_start_handle, service_end_handle, service_uuid in services_data:
            characteristics_data = self._execute_ble_operation(
                lambda: self._ble.gattc_discover_characteristics(self._conn_handle, service_start_handle, service_end_handle)
            )
            for _, characteristic_def_handle, characteristic_value_handle, _, characteristic_uuid in characteristics_data:
                if characteristic_uuid == _STATE_CHARACTERISTIC_UUID:
                    descriptors_data = self._execute_ble_operation(
                        lambda: self._ble.gattc_discover_descriptors(
                            self._conn_handle,
                            characteristic_value_handle,
                            characteristic_def_handle,
                        )
                    )
                    # Enable notifications
                    for _, descriptor_dsc_handle, descriptor_uuid in descriptors_data:
                        if descriptor_uuid == _CCCD_UUID:
                            self._execute_ble_operation(lambda: self._ble.gattc_write(self._conn_handle, descriptor_dsc_handle, b"\x01\x00", True))
                            break
                    # got value handle
                    self._state_value_handle = characteristic_value_handle
                elif characteristic_uuid == _TX_POWER_CHARACTERISTIC_UUID:
                    self._tx_power_value_handle = characteristic_value_handle
                elif characteristic_uuid == _DEVICE_INFO_MODEL_NUMBER_STRING_UUID:
                    result = self._execute_ble_operation(lambda: self._ble.gattc_read(self._conn_handle, characteristic_value_handle))
                    self._model_number = bytes(result[0][2]).decode("utf-8")

        self._is_connected = True

    def _execute_ble_operation(self, action):
        self._event.clear()
        self._action_result_data = []
        action()
        asyncio.run(self._event.wait())
        return self._action_result_data

    def _fetch_inputs(self):
        with self._lock:
            result = self._state
            self._state = None
        return result

    def set_tx_power(self, tx_power):
        self._execute_ble_operation(lambda: self._ble.gattc_write(self._conn_handle, self._tx_power_value_handle, struct.pack("b", tx_power), True))

    @property
    def model_number(self):
        return self._model_number

    @property
    def is_connected(self):
        return self._is_connected
