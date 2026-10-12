import bluetooth
import struct
import aioble
import asyncio
from micropython import const

__version__ = "4.0.0"

BUTTON_UP = const(1 << 0)
BUTTON_DOWN = const(1 << 1)
BUTTON_LEFT = const(1 << 2)
BUTTON_RIGHT = const(1 << 3)
BUTTON_SQUARE_X = const(1 << 4)
BUTTON_TRIANGLE_Y = const(1 << 5)
BUTTON_CROSS_A = const(1 << 6)
BUTTON_CIRCLE_B = const(1 << 7)
BUTTON_L1 = const(1 << 8)
BUTTON_L2 = const(1 << 9)
BUTTON_L3 = const(1 << 10)
BUTTON_R1 = const(1 << 11)
BUTTON_R2 = const(1 << 12)
BUTTON_R3 = const(1 << 13)
BUTTON_SELECT = const(1 << 14)
BUTTON_START = const(1 << 15)
BUTTON_HOME = const(1 << 16)

AXIS_LEFT_STICK_X = const(0)
AXIS_LEFT_STICK_Y = const(1)
AXIS_RIGHT_STICK_X = const(2)
AXIS_RIGHT_STICK_Y = const(3)

AXIS_CENTER = const(0x80)

_GAP_SERVICE_UUID = bluetooth.UUID(0x1800)
_GAP_DEVICE_NAME_UUID = bluetooth.UUID(0x2A00)

_INPUTS_SERVICE_UUID = bluetooth.UUID(0xFFA0)
_INPUTS_CHARACTERISTIC_UUID = bluetooth.UUID(0xFFA1)

_DEVICE_INFO_SERVICE_UUID = bluetooth.UUID(0x180A)
_MODEL_NUMBER_STRING_UUID = bluetooth.UUID(0x2A24)
_SERIAL_NUMBER_STRING_UUID = bluetooth.UUID(0x2A25)
_FIRMWARE_REVISION_STRING_UUID = bluetooth.UUID(0x2A26)
_MANUFACTURER_NAME_STRING_UUID = bluetooth.UUID(0x2A29)

_MANUFACTURER_HEADER = "CodexPad".encode("utf-8")

_BUTTON_STATE_UNPACK_FMT = "I"
_FIRMWARE_VERSION_UNPACK_FMT = "BBB"
_MANUFACTURER_HEADER_UNPACK_FMT = "B" * len(_MANUFACTURER_HEADER)

_MANUFACTURER_FIRMWARE_VERSION_LENGTH = len(_FIRMWARE_VERSION_UNPACK_FMT)
_MANUFACTURER_DATA_LENGTH = len(_MANUFACTURER_HEADER) + _MANUFACTURER_FIRMWARE_VERSION_LENGTH + 4 + 1
_MANUFACTURER_DATA_UNPACK_FMT = "<" + _MANUFACTURER_HEADER_UNPACK_FMT + _FIRMWARE_VERSION_UNPACK_FMT + _BUTTON_STATE_UNPACK_FMT + "B"

_AXIS_VALUE_UNPACK_FMT = "BBBB"
_INPUTS_UNPACK_FMT = "<" + _BUTTON_STATE_UNPACK_FMT + _AXIS_VALUE_UNPACK_FMT
_INPUTS_DATA_LENGTH = 8


class CodexPadNotFoundError(Exception):
    pass

def _validate_address(address: str):
    parts = address.split(':')
    if len(parts) != 6:
        raise ValueError(f"address must be in format 'XX:XX:XX:XX:XX:XX', got '{address}'")

    for part in parts:
        if len(part) != 2:
            raise ValueError(f"address: '{part}' is not a 2-char hex byte")
        for c in part:
            if c not in '0123456789ABCDEFabcdef':
                raise ValueError(f"address: '{address}' contains non-hex char '{c}'")

class CodexPadClient:

    class InputState:

        def __init__(self):
            self.button_mask = 0
            self.axes = [AXIS_CENTER, AXIS_CENTER, AXIS_CENTER, AXIS_CENTER]

        def parse_and_set(self, data: bytes):
            if not data or len(data) != _INPUTS_DATA_LENGTH:
                return
            [
                self.button_mask,
                self.axes[AXIS_LEFT_STICK_X],
                self.axes[AXIS_LEFT_STICK_Y],
                self.axes[AXIS_RIGHT_STICK_X],
                self.axes[AXIS_RIGHT_STICK_Y],
            ] = struct.unpack(_INPUTS_UNPACK_FMT, data)

        def assign(self, other):
            self.button_mask = other.button_mask
            self.axes = other.axes[:]

    def __init__(self):
        self._remote_model_number = None
        self._remote_device_name = None
        self._remote_firmware_version = None
        self._connection = None
        self._inputs_characteristic = None
        self._prev_inputs = CodexPadClient.InputState()
        self._current_inputs = CodexPadClient.InputState()

    async def _reset(self):
        self._remote_model_number = None
        self._remote_device_name = None
        self._remote_firmware_version = None
        if self._connection:
            await self._connection.disconnect()
        self._connection = None
        self._inputs_characteristic = None
        self._prev_inputs = CodexPadClient.InputState()
        self._current_inputs = CodexPadClient.InputState()

    def connect_by_button_mask(self, button_mask, scan_duration_ms=1000, connect_timeout_ms=5000):
        if not isinstance(button_mask, int):
            raise TypeError(f"button_mask must be int, got {type(button_mask).__name__}")

        asyncio.get_event_loop().run_until_complete(self._connect_by_button_mask(button_mask, scan_duration_ms, connect_timeout_ms))

    async def _connect_by_button_mask(self, button_mask, scan_duration_ms, connect_timeout_ms):
        rssi = None
        device = None
        async with aioble.scan(scan_duration_ms, interval_us=50000, window_us=20000, active=True) as scanner:
            async for result in scanner:
                if not result.name() or not result.name().startswith("CodexPad-"):
                    continue

                if not result.manufacturer():
                    continue

                if not result.rssi:
                    continue

                mfr_data = list(result.manufacturer(0xFFFF))
                if mfr_data is None or len(mfr_data) == 0:
                    continue

                manufacturer_data = mfr_data[0][1]

                if len(manufacturer_data) < _MANUFACTURER_DATA_LENGTH:
                    continue

                unpacked = struct.unpack(_MANUFACTURER_DATA_UNPACK_FMT, manufacturer_data[:_MANUFACTURER_DATA_LENGTH])

                header_bytes = bytes(unpacked[: len(_MANUFACTURER_HEADER)])

                if header_bytes != _MANUFACTURER_HEADER:
                    continue

                firmware_version = bytes(unpacked[len(_MANUFACTURER_HEADER) : len(_MANUFACTURER_HEADER) + _MANUFACTURER_FIRMWARE_VERSION_LENGTH])
                # print(f"Found CodexPad device: {result.name()}, address: {result.device}, rssi: {result.rssi}, manufacturer_data: {manufacturer_data}, firmware_version: {firmware_version}")

                current_button_mask = unpacked[len(_MANUFACTURER_HEADER) + _MANUFACTURER_FIRMWARE_VERSION_LENGTH]

                if current_button_mask != button_mask:
                    continue

                button_mask_duration_seconds = unpacked[-1]
                # print(f"button_states_duration_seconds: {button_states_duration_seconds}")

                if firmware_version[0] > 1 and button_mask_duration_seconds < 1:
                    continue

                if device is None or result.rssi > rssi:
                    rssi = result.rssi
                    device = result.device

                    # print(
                    #     f"Found CodexPad device: {result.name()}, address: {result.device}, rssi: {result.rssi}, manufacturer_data: {manufacturer_data}, button_state: 0x{button_state:08X}"
                    # )
        if not device:
            raise CodexPadNotFoundError(f"No CodexPad device found with button mask 0x{button_mask:08X}")

        await self._connect(device, connect_timeout_ms)

    def connect_by_address(self, address, timeout_ms):
        if not isinstance(address, str):
            raise TypeError(f"address must be str, got {type(address).__name__}")
        _validate_address(address)
        asyncio.get_event_loop().run_until_complete(self._connect(aioble.Device(aioble.ADDR_PUBLIC, address), timeout_ms))

    async def _connect(self, device, timeout_ms):
        await self._reset()
        try:
            self._connection = await device.connect(timeout_ms=timeout_ms, scan_duration_ms=1000)

            gap_service = await self._connection.service(_GAP_SERVICE_UUID)
            device_name_characteristic = await gap_service.characteristic(_GAP_DEVICE_NAME_UUID)
            self._remote_device_name = (await device_name_characteristic.read()).decode("utf-8")

            device_info_service = await self._connection.service(_DEVICE_INFO_SERVICE_UUID)
            model_number_characteristic = await device_info_service.characteristic(_MODEL_NUMBER_STRING_UUID)
            self._remote_model_number = (await model_number_characteristic.read()).decode("utf-8")

            firmware_revision_characteristic = await device_info_service.characteristic(_FIRMWARE_REVISION_STRING_UUID)
            self._remote_firmware_version = tuple(struct.unpack(_FIRMWARE_VERSION_UNPACK_FMT, (await firmware_revision_characteristic.read())))

            inputs_service = await self._connection.service(_INPUTS_SERVICE_UUID)
            inputs_characteristic = await inputs_service.characteristic(_INPUTS_CHARACTERISTIC_UUID)
            await inputs_characteristic.subscribe(notify=True)
            self._inputs_characteristic = inputs_characteristic
        except Exception as e:
            await self._reset()
            raise e

    def disconnect(self):
        asyncio.get_event_loop().run_until_complete(self._reset())

    @property
    def remote_device_name(self):
        return self._remote_device_name

    @property
    def remote_model_number(self):
        return self._remote_model_number

    @property
    def remote_firmware_version(self):
        return self._remote_firmware_version

    @property
    def remote_firmware_version_major(self):
        return self._remote_firmware_version[0]

    @property
    def remote_firmware_version_minor(self):
        return self._remote_firmware_version[1]

    @property
    def remote_firmware_version_patch(self):
        return self._remote_firmware_version[2]

    @property
    def remote_address(self):
        return self._connection.device.addr_hex().upper()

    @property
    def is_connected(self):
        return self._connection and self._connection.is_connected()

    def update(self):
        self._prev_inputs.assign(self._current_inputs)

        if self._connection is None or self._inputs_characteristic is None or not self._connection.is_connected():
            self._current_inputs = CodexPadClient.InputState()
            return

        try:
            self._current_inputs.parse_and_set(asyncio.get_event_loop().run_until_complete(self._inputs_characteristic.notified(timeout_ms=1)))
        except Exception:
            pass

    def pressed(self, button):
        return ((self._prev_inputs.button_mask & button) == 0) and ((self._current_inputs.button_mask & button) != 0)

    def released(self, button):
        return ((self._prev_inputs.button_mask & button) != 0) and ((self._current_inputs.button_mask & button) == 0)

    def holding(self, button):
        return ((self._prev_inputs.button_mask & button) != 0) and ((self._current_inputs.button_mask & button) != 0)

    def down(self, button):
        return (self._current_inputs.button_mask & button) == button

    @property
    def button_mask(self) -> int:
        return self._current_inputs.button_mask

    def axis_value(self, axis):
        return self._current_inputs.axes[axis]

    @property
    def axes(self):
        return tuple(self._current_inputs.axes)

    def _has_axis_value_changed_significantly(self, prev_value, current_value, threshold):
        return prev_value != current_value and (current_value == 0 or current_value == 255 or abs(current_value - prev_value) >= threshold)

    def has_axis_value_changed(self, axis, threshold):
        return self._has_axis_value_changed_significantly(self._prev_inputs.axes[axis], self._current_inputs.axes[axis], threshold)
