import asyncio
import codex_pad

# Replace with your CodexPad device's Bluetooth device address
# 替换为你的 CodexPad 的 Bluetooth device address
_BLUETOOTH_DEVICE_ADDRESS = "0C:3D:5E:9D:80:DE"


# Connect to the CodexPad device
# 连接到 CodexPad 设备
def Connect(bluetooth_device_address):
    while True:
        try:
            print(f"Connecting to {bluetooth_device_address}")
            asyncio.run(codex_pad_obj.connect(bluetooth_device_address, timeout_ms=5000))
            print(f"Remote device name: {codex_pad_obj.remote_device_name}")
            print(f"Remote model number: {codex_pad_obj.remote_model_number}")
            print(
                f"Remote firmware version: {codex_pad_obj.remote_firmware_version_major}.{codex_pad_obj.remote_firmware_version_minor}.{codex_pad_obj.remote_firmware_version_patch}"
            )
            print(f"Remote Bluetooth Device Address: {codex_pad_obj.remote_bluetooth_device_address}")

            # 设置发射功率为0dBm
            # 发射功率影响通信距离和功耗：功率越高，通信距离越远，但功耗也越大
            # 建议根据实际应用场景选择合适的功率等级以平衡距离和电池寿命
            # Set transmission power to 0dBm
            # Transmission power affects communication range and power consumption:
            # Higher power provides longer range but consumes more battery
            # Choose appropriate power level based on your application to balance range and battery life
            asyncio.run(codex_pad_obj.set_remote_tx_power(codex_pad.TX_POWER_0_DBM))
            print("Connected")
            return
        except asyncio.TimeoutError:
            print("Connection timed out, trying again...")
        except Exception as e:
            print(f"Connection failed: {e}")


# Set up
print("codex_pad library version:", codex_pad.__version__)
codex_pad_obj = codex_pad.CodexPad()

Connect(_BLUETOOTH_DEVICE_ADDRESS)

# Main loop
while True:
    # 重要：update()方法必须在循环中尽可能频繁地调用，不能添加延时
    # 该方法负责处理所有接收到的蓝牙数据包，延时会导致数据丢失和响应延迟
    # 对于实时控制应用，必须保持高频率调用以确保及时响应手柄输入
    # Important: update() method must be called as frequently as possible in the loop, no delays should be added
    # This method processes all received Bluetooth packets, delays will cause data loss and response lag
    # For real-time control applications, high-frequency calls are essential to ensure prompt response to gamepad input
    asyncio.run(codex_pad_obj.update())

    if not codex_pad_obj.is_connected:
        print("Disconnected from device, trying to reconnect...")
        Connect(_BLUETOOTH_DEVICE_ADDRESS)
        continue

    print(
        f"Up:{int(codex_pad_obj.button_state(codex_pad.BUTTON_UP))},",
        f"Down:{int(codex_pad_obj.button_state(codex_pad.BUTTON_DOWN))},",
        f"Left:{int(codex_pad_obj.button_state(codex_pad.BUTTON_LEFT))},",
        f"Right:{int(codex_pad_obj.button_state(codex_pad.BUTTON_RIGHT))},",
        f"SquareX:{int(codex_pad_obj.button_state(codex_pad.BUTTON_SQUARE_X))},",
        f"TriangleY:{int(codex_pad_obj.button_state(codex_pad.BUTTON_TRIANGLE_Y))},",
        f"CrossA:{int(codex_pad_obj.button_state(codex_pad.BUTTON_CROSS_A))},",
        f"CircleB:{int(codex_pad_obj.button_state(codex_pad.BUTTON_CIRCLE_B))}",
        f"L1:{int(codex_pad_obj.button_state(codex_pad.BUTTON_L1))},",
        f"L2:{int(codex_pad_obj.button_state(codex_pad.BUTTON_L2))},",
        f"L3:{int(codex_pad_obj.button_state(codex_pad.BUTTON_L3))},",
        f"R1:{int(codex_pad_obj.button_state(codex_pad.BUTTON_R1))},",
        f"R2:{int(codex_pad_obj.button_state(codex_pad.BUTTON_R2))},",
        f"R3:{int(codex_pad_obj.button_state(codex_pad.BUTTON_R3))},",
        f"Select:{int(codex_pad_obj.button_state(codex_pad.BUTTON_SELECT))},",
        f"Start:{int(codex_pad_obj.button_state(codex_pad.BUTTON_START))},",
        f"Home:{int(codex_pad_obj.button_state(codex_pad.BUTTON_HOME))}",
        f"L(X:{codex_pad_obj.axis_value(codex_pad.AXIS_LEFT_STICK_X):>3},",
        f"Y:{codex_pad_obj.axis_value(codex_pad.AXIS_LEFT_STICK_Y):>3}),",
        f"R(X:{codex_pad_obj.axis_value(codex_pad.AXIS_RIGHT_STICK_X):>3},",
        f"Y:{codex_pad_obj.axis_value(codex_pad.AXIS_RIGHT_STICK_Y):>3})",
    )
