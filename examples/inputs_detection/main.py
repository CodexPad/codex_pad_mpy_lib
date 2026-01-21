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


def button_to_string(button):
    """将按钮常量转换为可读的字符串名称"""
    """Convert button constant to readable string name"""
    return {
        BUTTON_UP: "Up",
        BUTTON_DOWN: "Down",
        BUTTON_LEFT: "Left",
        BUTTON_RIGHT: "Right",
        BUTTON_SQUARE_X: "SquareX",
        BUTTON_TRIANGLE_Y: "TriangleY",
        BUTTON_CROSS_A: "CrossA",
        BUTTON_CIRCLE_B: "CircleB",
        BUTTON_L1: "L1",
        BUTTON_L2: "L2",
        BUTTON_L3: "L3",
        BUTTON_R1: "R1",
        BUTTON_R2: "R2",
        BUTTON_R3: "R3",
        BUTTON_SELECT: "Select",
        BUTTON_START: "Start",
        BUTTON_HOME: "Home",
    }[button]


print(f"setup")
print(f"codex_pad lib version: {codex_pad.__version__}")
ble = bluetooth.BLE()
codex_pad_obj = codex_pad.CodexPad(ble)

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

# 主循环 - 检测状态变化
# Main loop - detect state changes
while True:
    # 重要：update()方法必须在循环中尽可能频繁地调用，不能添加延时
    # 该方法负责处理所有接收到的蓝牙数据包，延时会导致数据丢失和响应延迟
    # 对于实时控制应用，必须保持高频率调用以确保及时响应手柄输入
    # Important: update() method must be called as frequently as possible in the loop, no delays should be added
    # This method processes all received Bluetooth packets, delays will cause data loss and response lag
    # For real-time control applications, high-frequency calls are essential to ensure prompt response to gamepad input
    codex_pad_obj.update()

    # 检测所有按钮的状态变化
    # 使用pressed(), released(), holding()方法检测按钮的不同状态
    # Detect state changes for all buttons
    # Use pressed(), released(), holding() methods to detect different button states
    for button in (
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
    ):
        # 检测按钮是否刚刚按下（从弹起变为按下）
        # Check if button was just pressed (transition from released to pressed)
        if codex_pad_obj.pressed(button):
            print(f"Button {button_to_string(button)}: pressed")

        # 检测按钮是否刚刚释放（从按下变为弹起）
        # Check if button was just released (transition from pressed to released)
        elif codex_pad_obj.released(button):
            print(f"Button {button_to_string(button)}: released")

        # 检测按钮是否持续按下状态
        # Check if button is holding
        elif codex_pad_obj.holding(button):
            print(f"Button {button_to_string(button)}: holding")

    # 检测摇杆轴值是否发生了有效变化（使用阈值避免微小抖动）
    # 阈值设置为2，只有当摇杆值变化达到或超过2个单位时才认为是有效变化
    # Check if joystick axis values have changed significantly (using threshold to avoid minor jitter)
    # Threshold is set to 2, only consider changes equal to or greater than 2 units as significant
    AXIS_VALUE_CHANGE_THRESHOLD = 2

    # 检测摇杆X轴或Y轴是否有显著变化
    # Check if stick X or Y axis has significant change
    if (
        codex_pad_obj.has_axis_value_changed(AXIS_LEFT_STICK_X, AXIS_VALUE_CHANGE_THRESHOLD)
        or codex_pad_obj.has_axis_value_changed(AXIS_LEFT_STICK_Y, AXIS_VALUE_CHANGE_THRESHOLD)
        or codex_pad_obj.has_axis_value_changed(AXIS_RIGHT_STICK_X, AXIS_VALUE_CHANGE_THRESHOLD)
        or codex_pad_obj.has_axis_value_changed(AXIS_RIGHT_STICK_Y, AXIS_VALUE_CHANGE_THRESHOLD)
    ):
        print(
            "Left stick axis values:",
            f"[X: {codex_pad_obj.axis_value(AXIS_LEFT_STICK_X):>3}],",
            f"[Y: {codex_pad_obj.axis_value(AXIS_LEFT_STICK_Y):>3}]",
            f", Right stick axis values:",
            f"[X: {codex_pad_obj.axis_value(AXIS_RIGHT_STICK_X):>3}],",
            f"[Y: {codex_pad_obj.axis_value(AXIS_RIGHT_STICK_Y):>3}]",
        )
