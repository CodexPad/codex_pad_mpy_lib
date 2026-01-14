import bluetooth
import codex_pad

from codex_pad import (
    BUTTON_UP,
    BUTTON_DOWN,
    BUTTON_LEFT,
    BUTTON_RIGHT,
    BUTTON_SQUARE_X,
    BUTTON_TRIANGLE_Y,
    BUTTON_CROSS_A,
    BUTTON_CIRCLE_B,
    BUTTON_L1,
    BUTTON_L2,
    BUTTON_L3,
    BUTTON_R1,
    BUTTON_R2,
    BUTTON_R3,
    BUTTON_SELECT,
    BUTTON_START,
    BUTTON_HOME,
)

from codex_pad import (
    AXIS_LEFT_STICK_X,
    AXIS_LEFT_STICK_Y,
    AXIS_RIGHT_STICK_X,
    AXIS_RIGHT_STICK_Y,
)

from codex_pad import (
    TX_POWER_MINUS_16_DBM,  # -16dBm
    TX_POWER_MINUS_12_DBM,  # -12dBm
    TX_POWER_MINUS_8_DBM,  # -8dBm
    TX_POWER_MINUS_5_DBM,  # -5dBm
    TX_POWER_MINUS_3_DBM,  # -3dBm
    TX_POWER_MINUS_1_DBM,  # -1dBm
    TX_POWER_0_DBM,  # 0dBm
    TX_POWER_1_DBM,  # 1dBm
    TX_POWER_2_DBM,  # 2dBm
    TX_POWER_3_DBM,  # 3dBm
    TX_POWER_4_DBM,  # 4dBm
    TX_POWER_5_DBM,  # 5dBm
    TX_POWER_6_DBM,  # 6dBm
)

print(f"setup")
print(f"codex_pad lib version: {codex_pad.__version__}")
codex_pad_obj = codex_pad.CodexPad(bluetooth.BLE())

print("begin connecting")
# 连接到指定MAC地址的手柄
# Connect to the CodexPad with specified MAC address
codex_pad_obj.connect("E4:66:E5:A2:24:5D")

print(f"connected, model number is {codex_pad_obj.model_number}")

# 设置发射功率为0dBm
# 发射功率影响通信距离和功耗：功率越高，通信距离越远，但功耗也越大
# 建议根据实际应用场景选择合适的功率等级以平衡距离和电池寿命
# Set transmission power to 0dBm
# Transmission power affects communication range and power consumption:
# Higher power provides longer range but consumes more battery
# Choose appropriate power level based on your application to balance range and battery life
codex_pad_obj.set_tx_power(TX_POWER_0_DBM)

# 主循环 - 持续轮询手柄状态
# Main loop - continuously poll gamepad state
while True:
    # 重要：update()方法必须在循环中尽可能频繁地调用，不能添加延时
    # 该方法负责处理所有接收到的蓝牙数据包，延时会导致数据丢失和响应延迟
    # 对于实时控制应用，必须保持高频率调用以确保及时响应手柄输入
    # Important: update() method must be called as frequently as possible in the loop, no delays should be added
    # This method processes all received Bluetooth packets, delays will cause data loss and response lag
    # For real-time control applications, high-frequency calls are essential to ensure prompt response to gamepad input
    codex_pad_obj.update()

    print(
        f"Up:{int(codex_pad_obj.button_state(BUTTON_UP))},",
        f"Down:{int(codex_pad_obj.button_state(BUTTON_DOWN))},",
        f"Left:{int(codex_pad_obj.button_state(BUTTON_LEFT))},",
        f"Right:{int(codex_pad_obj.button_state(BUTTON_RIGHT))},",
        f"SquareX:{int(codex_pad_obj.button_state(BUTTON_SQUARE_X))},",
        f"TriangleY:{int(codex_pad_obj.button_state(BUTTON_TRIANGLE_Y))},",
        f"CrossA:{int(codex_pad_obj.button_state(BUTTON_CROSS_A))},",
        f"CircleB:{int(codex_pad_obj.button_state(BUTTON_CIRCLE_B))}",
        f"L1:{int(codex_pad_obj.button_state(BUTTON_L1))},",
        f"L2:{int(codex_pad_obj.button_state(BUTTON_L2))},",
        f"L3:{int(codex_pad_obj.button_state(BUTTON_L3))},",
        f"R1:{int(codex_pad_obj.button_state(BUTTON_R1))},",
        f"R2:{int(codex_pad_obj.button_state(BUTTON_R2))},",
        f"R3:{int(codex_pad_obj.button_state(BUTTON_R3))},",
        f"Select:{int(codex_pad_obj.button_state(BUTTON_SELECT))},",
        f"Start:{int(codex_pad_obj.button_state(BUTTON_START))},",
        f"Home:{int(codex_pad_obj.button_state(BUTTON_HOME))}",
        f"LAxis X:{codex_pad_obj.axis_value(AXIS_LEFT_STICK_X):>3},",
        f"Y:{codex_pad_obj.axis_value(AXIS_LEFT_STICK_Y):>3},",
        f"RAxis X:{codex_pad_obj.axis_value(AXIS_RIGHT_STICK_X):>3},",
        f"Y:{codex_pad_obj.axis_value(AXIS_RIGHT_STICK_Y):>3}",
    )
