"""
CodexPadC10 基础轮询示例
CodexPadC10 Basic Polling Example

本示例演示如何使用CodexPadC10 BLE手柄进行基础状态轮询
This example demonstrates how to perform basic state polling with CodexPadC10 BLE gamepad
"""

import bluetooth

from codex_pad_c10 import (
    BUTTON_A,  # A按钮 | A button
    BUTTON_B,  # B按钮 | B button
    BUTTON_X,  # X按钮 | X button
    BUTTON_Y,  # Y按钮 | Y button
    BUTTON_START,  # START按钮 | START button
    BUTTON_L3,  # 左摇杆按下触发 | LEFT_STICK button press
    AXIS_LEFT_STICK_X,  # 左摇杆X轴 | Left stick X axis
    AXIS_LEFT_STICK_Y,  # 左摇杆Y轴 | Left stick Y axis
    CodexPadC10,  # CodexPadC10类 | CodexPadC10 class
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

print("setup")
# 初始化BLE和CodexPadC10实例
# Initialize BLE and CodexPadC10 instance
codex_pad = CodexPadC10(bluetooth.BLE())

print("begin connecting")
# 连接到指定MAC地址的手柄
# Connect to the CodexPad with specified MAC address
codex_pad.connect("E4:66:E5:A2:24:5D")

print(f"connected, model number is {codex_pad.model_number}")

# 设置发射功率为0dBm
# 发射功率影响通信距离和功耗：功率越高，通信距离越远，但功耗也越大
# 建议根据实际应用场景选择合适的功率等级以平衡距离和电池寿命
# Set transmission power to 0dBm
# Transmission power affects communication range and power consumption:
# Higher power provides longer range but consumes more battery
# Choose appropriate power level based on your application to balance range and battery life
codex_pad.set_tx_power(TX_POWER_0_DBM)

# 主循环 - 持续轮询手柄状态
# Main loop - continuously poll gamepad state
while True:
    # 重要：update()方法必须在循环中尽可能频繁地调用，不能添加延时
    # 该方法负责处理所有接收到的蓝牙数据包，延时会导致数据丢失和响应延迟
    # 对于实时控制应用，必须保持高频率调用以确保及时响应手柄输入
    # Important: update() method must be called as frequently as possible in the loop, no delays should be added
    # This method processes all received Bluetooth packets, delays will cause data loss and response lag
    # For real-time control applications, high-frequency calls are essential to ensure prompt response to gamepad input
    codex_pad.update()

    # 获取各个按钮的状态，button_state()返回数字类型，1表示按下，0表示弹起
    # 注意：BUTTON_L3对应左摇杆按下操作，不是摇杆移动
    # Get button states, button_state() returns integer type, 1 means pressed, 0 means released
    # Note: BUTTON_L3 corresponds to left stick button press, not stick movement
    button_l3_state = codex_pad.button_state(BUTTON_L3)  # 左摇杆按下状态 | Left stick button state
    button_start_state = codex_pad.button_state(BUTTON_START)  # START按钮状态 | START button state
    button_x_state = codex_pad.button_state(BUTTON_X)  # X按钮状态 | X button state
    button_y_state = codex_pad.button_state(BUTTON_Y)  # Y按钮状态 | Y button state
    button_a_state = codex_pad.button_state(BUTTON_A)  # A按钮状态 | A button state
    button_b_state = codex_pad.button_state(BUTTON_B)  # B按钮状态 | B button state

    # 获取摇杆轴数据，axis_value()返回0~255的数值
    # 中间位置约为127，数值范围表示摇杆的偏移程度
    # Get joystick axis data, axis_value() returns value from 0 to 255
    # Center position is around 127, values represent stick deflection
    left_stick_x_axis_value = codex_pad.axis_value(AXIS_LEFT_STICK_X)  # 左摇杆X轴数值 | Left stick X axis value
    left_stick_y_axis_value = codex_pad.axis_value(AXIS_LEFT_STICK_Y)  # 左摇杆Y轴数值 | Left stick Y axis value

    # 打印当前状态 - 便于调试和监控手柄输入
    # Print current status - useful for debugging and monitoring gamepad input
    print(
        f"Button States: [L3: {button_l3_state}],",
        f"[START: {button_start_state}],",
        f"[X: {button_x_state}],",
        f"[Y: {button_y_state}],",
        f"[A: {button_a_state}],",
        f"[B: {button_b_state}],",
        f"Left stick axis values: [X: {left_stick_x_axis_value}], [Y: {left_stick_y_axis_value}]",
    )
