import asyncio
import codex_pad
import time

# Replace with your CodexPad device's Bluetooth device address
# 替换为你的 CodexPad 的 Bluetooth device address
_BLUETOOTH_DEVICE_ADDRESS = "E4:66:E5:A2:17:06"


# Connect to the CodexPad device
# 连接到 CodexPad 设备
def connect(address):
    while True:
        try:
            print(f"Connecting to {address}")
            codex_pad_client.connect_by_address(address, timeout_ms=2000)
            print(f"Remote device name: {codex_pad_client.remote_device_name}")
            print(f"Remote model number: {codex_pad_client.remote_model_number}")
            print(
                f"Remote firmware version: {codex_pad_client.remote_firmware_version_major}.{codex_pad_client.remote_firmware_version_minor}.{codex_pad_client.remote_firmware_version_patch}"
            )
            print(f"Remote address: {codex_pad_client.remote_address}")
            print("Connected")
            return
        except asyncio.TimeoutError:
            print("Connection timed out, trying again...")
        except TypeError as e:
            print(f"TypeError: {e}")
            raise e
        except ValueError as e:
            print(f"ValueError: {e}")
            raise e
        except Exception as e:
            print(f"Connection failed: {e}, trying again...")
            import aioble
            aioble.core.stop()

# Set up
print("codex_pad library version:", codex_pad.__version__)
codex_pad_client = codex_pad.CodexPadClient()
log_time = None

# Main loop
while True:
    # 重要：update()方法必须在循环中尽可能频繁地调用，不能添加延时
    # 该方法负责处理所有接收到的蓝牙数据包，延时会导致数据丢失和响应延迟
    # 对于实时控制应用，必须保持高频率调用以确保及时响应手柄输入
    # Important: update() method must be called as frequently as possible in the loop, no delays should be added
    # This method processes all received Bluetooth packets, delays will cause data loss and response lag
    # For real-time control applications, high-frequency calls are essential to ensure prompt response to gamepad input
    codex_pad_client.update()

    if not codex_pad_client.is_connected:
        print("Disconnected from device, trying to reconnect...")
        connect(_BLUETOOTH_DEVICE_ADDRESS)
        continue

    if not log_time or log_time + 50 < time.ticks_ms():
        log_message = f"Button mask: 0x{codex_pad_client.button_mask:08X},"
        log_message += f" L({codex_pad_client.axis_value(codex_pad.AXIS_LEFT_STICK_X):>3}, {codex_pad_client.axis_value(codex_pad.AXIS_LEFT_STICK_Y):>3})"
        log_message += f", R({codex_pad_client.axis_value(codex_pad.AXIS_RIGHT_STICK_X):>3}, {codex_pad_client.axis_value(codex_pad.AXIS_RIGHT_STICK_Y):>3})"

        if codex_pad_client.down(codex_pad.BUTTON_UP):
            log_message += ", Up"

        if codex_pad_client.down(codex_pad.BUTTON_DOWN):
            log_message += ", Down"

        if codex_pad_client.down(codex_pad.BUTTON_LEFT):
            log_message += ", Left"

        if codex_pad_client.down(codex_pad.BUTTON_RIGHT):
            log_message += ", Right"

        if codex_pad_client.down(codex_pad.BUTTON_SQUARE_X):
            log_message += ", Square(X)"

        if codex_pad_client.down(codex_pad.BUTTON_TRIANGLE_Y):
            log_message += ", Triangle(Y)"

        if codex_pad_client.down(codex_pad.BUTTON_CROSS_A):
            log_message += ", Cross(A)"

        if codex_pad_client.down(codex_pad.BUTTON_CIRCLE_B):
            log_message += ", Circle(B)"

        if codex_pad_client.down(codex_pad.BUTTON_L1):
            log_message += ", L1"

        if codex_pad_client.down(codex_pad.BUTTON_L2):
            log_message += ", L2"

        if codex_pad_client.down(codex_pad.BUTTON_L3):
            log_message += ", L3"

        if codex_pad_client.down(codex_pad.BUTTON_R1):
            log_message += ", R1"

        if codex_pad_client.down(codex_pad.BUTTON_R2):
            log_message += ", R2"

        if codex_pad_client.down(codex_pad.BUTTON_R3):
            log_message += ", R3"

        if codex_pad_client.down(codex_pad.BUTTON_SELECT):
            log_message += ", Select"

        if codex_pad_client.down(codex_pad.BUTTON_START):
            log_message += ", Start"

        if codex_pad_client.down(codex_pad.BUTTON_HOME):
            log_message += ", Home"

        print(log_message)

        log_time = time.ticks_ms()
