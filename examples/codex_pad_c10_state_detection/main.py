"""
CodexPadC10 状态检测示例
CodexPadC10 State Detection Example

本示例演示如何使用CodexPadC10 BLE手柄进行状态变化检测
This example demonstrates how to perform state change detection with CodexPadC10 BLE gamepad
"""

import codex_pad_c10
import bluetooth

# 导入按钮和摇杆轴常量
# Import button and axis constants
from codex_pad_c10 import (
    BUTTON_A,  # A按钮 | A button
    BUTTON_B,  # B按钮 | B button
    BUTTON_X,  # X按钮 | X button
    BUTTON_Y,  # Y按钮 | Y button
    BUTTON_START,  # START按钮 | START button
    BUTTON_L3,  # 左摇杆按下触发 | LEFT_STICK button press
    AXIS_LEFT_STICK_X,  # 左摇杆X轴 | Left stick X axis
    AXIS_LEFT_STICK_Y,  # 左摇杆Y轴 | Left stick Y axis
)

# 导入发射功率常量
# Import transmission power constants
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
        BUTTON_A: "A",
        BUTTON_B: "B",
        BUTTON_X: "X",
        BUTTON_Y: "Y",
        BUTTON_START: "START",
        BUTTON_L3: "L3",
    }[button]


print("setup")
# 初始化BLE和CodexPadC10实例
# Initialize BLE and CodexPadC10 instance
ble = bluetooth.BLE()
codex_pad_c10_instance = codex_pad_c10.CodexPadC10(ble)

print("begin connecting")
# 连接到指定MAC地址的手柄
# Connect to the CodexPad with specified MAC address
codex_pad_c10_instance.connect("E4:66:E5:A2:24:5D")

print(f"connected, model number is {codex_pad_c10_instance.model_number}")

# 设置发射功率为0dBm
# 发射功率影响通信距离和功耗：功率越高，通信距离越远，但功耗也越大
# 建议根据实际应用场景选择合适的功率等级以平衡距离和电池寿命
# Set transmission power to 0dBm
# Transmission power affects communication range and power consumption:
# Higher power provides longer range but consumes more battery
# Choose appropriate power level based on your application to balance range and battery life
codex_pad_c10_instance.set_tx_power(TX_POWER_0_DBM)

# 主循环 - 检测状态变化
# Main loop - detect state changes
while True:
    # 重要：update()方法必须在循环中尽可能频繁地调用，不能添加延时
    # 该方法负责处理所有接收到的蓝牙数据包，延时会导致数据丢失和响应延迟
    # 对于实时控制应用，必须保持高频率调用以确保及时响应手柄输入
    # Important: update() method must be called as frequently as possible in the loop, no delays should be added
    # This method processes all received Bluetooth packets, delays will cause data loss and response lag
    # For real-time control applications, high-frequency calls are essential to ensure prompt response to gamepad input
    codex_pad_c10_instance.update()

    # 检测所有按钮的状态变化
    # 使用pressed(), released(), holding()方法检测按钮的不同状态
    # Detect state changes for all buttons
    # Use pressed(), released(), holding() methods to detect different button states
    for button in (
        BUTTON_A,
        BUTTON_B,
        BUTTON_X,
        BUTTON_Y,
        BUTTON_START,
        BUTTON_L3,
    ):
        # 检测按钮是否刚刚按下（从弹起变为按下）
        # Check if button was just pressed (transition from released to pressed)
        if codex_pad_c10_instance.pressed(button):
            print(f"Button {button_to_string(button)}: pressed")

        # 检测按钮是否刚刚释放（从按下变为弹起）
        # Check if button was just released (transition from pressed to released)
        elif codex_pad_c10_instance.released(button):
            print(f"Button {button_to_string(button)}: released")

        # 检测按钮是否持续按下状态
        # Check if button is holding
        elif codex_pad_c10_instance.holding(button):
            print(f"Button {button_to_string(button)}: holding")

    # 检测摇杆轴值是否发生了有效变化（使用阈值避免微小抖动）
    # 阈值设置为2，只有当摇杆值变化达到或超过2个单位时才认为是有效变化
    # Check if joystick axis values have changed significantly (using threshold to avoid minor jitter)
    # Threshold is set to 2, only consider changes equal to or greater than 2 units as significant
    AXIS_VALUE_CHANGE_THRESHOLD = 2

    # 检测左摇杆X轴或Y轴是否有显著变化
    # Check if left stick X or Y axis has significant change
    if codex_pad_c10_instance.has_axis_value_changed(AXIS_LEFT_STICK_X, AXIS_VALUE_CHANGE_THRESHOLD) or codex_pad_c10_instance.has_axis_value_changed(
        AXIS_LEFT_STICK_Y, AXIS_VALUE_CHANGE_THRESHOLD
    ):
        print(
            "Left stick axis values:",
            f"[X: {codex_pad_c10_instance.axis_value(AXIS_LEFT_STICK_X)}],",
            f"[Y: {codex_pad_c10_instance.axis_value(AXIS_LEFT_STICK_Y)}]",
        )
