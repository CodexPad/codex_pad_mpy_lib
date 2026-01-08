from codex_pad import CodexPad
from micropython import const

# 按钮常量定义 - 使用位掩码表示不同按钮
# Button constants definition - using bit masks for different buttons
BUTTON_L3 = const(1 << 0)  # 左摇杆按下按钮 | Left stick press button
BUTTON_START = const(1 << 1)  # START按钮 | START button
BUTTON_X = const(1 << 2)  # X按钮 | X button
BUTTON_Y = const(1 << 3)  # Y按钮 | Y button
BUTTON_A = const(1 << 5)  # A按钮 | A button
BUTTON_B = const(1 << 4)  # B按钮 | B button

# 摇杆轴常量定义
# Joystick axis constants definition
AXIS_LEFT_STICK_X = const(0)  # 左摇杆X轴 | Left stick X axis
AXIS_LEFT_STICK_Y = const(1)  # 左摇杆Y轴 | Left stick Y axis


class CodexPadC10(CodexPad):
    """CodexPad C10类，继承自CodexPad基类"""

    """CodexPad C10 class, inherits from CodexPad base class"""

    def __init__(self, ble):
        """初始化C10手柄实例"""
        """Initialize C10 gamepad instance"""
        super().__init__(ble)
        self._prev_inputs = (0, 127, 127)  # 前一个输入值 | Previous input value
        self._current_inputs = (0, 127, 127)  # 当前输入值 | Current input value

    def connect(self, mac_address):
        """连接到指定MAC地址的手柄，验证型号为C10"""
        """Connect to gamepad with specified MAC address, verify model is C10"""
        super().connect(mac_address)
        if not self._model_number or self._model_number != "C10":
            raise Exception(f"Model number is {self._model_number} not C10")

    def update(self):
        """更新手柄输入状态，需要在主循环中持续调用"""
        """Update gamepad input state, must be called continuously in main loop"""
        self._prev_inputs = self._current_inputs
        new_inputs = self._fetch_inputs()

        if new_inputs:
            self._current_inputs = new_inputs

    def pressed(self, button):
        """检测按钮是否刚刚按下（从弹起变为按下）"""
        """Check if button was just pressed (transition from released to pressed)"""
        return (self._prev_inputs[0] & button) == 0 and (self._current_inputs[0] & button) != 0

    def released(self, button):
        """检测按钮是否刚刚释放（从按下变为弹起）"""
        """Check if button was just released (transition from pressed to released)"""
        return (self._prev_inputs[0] & button) != 0 and (self._current_inputs[0] & button) == 0

    def holding(self, button):
        """检测按钮是否持续按下状态"""
        """Check if button is continuously pressed"""
        return (self._prev_inputs[0] & button) != 0 and (self._current_inputs[0] & button) != 0

    def button_states(self):
        """获取所有按钮的完整状态位掩码"""
        """Get complete button state bitmask"""
        return self._current_inputs[0]

    def button_state(self, button):
        """获取指定按钮的当前状态（1=按下，0=弹起）"""
        """Get current state of specified button (1=pressed, 0=released)"""
        return 0 if (self._current_inputs[0] & button) == 0 else 1

    def axis_value(self, axis):
        """获取指定摇杆轴的当前值（0-255）"""
        """Get current value of specified joystick axis (0-255)"""
        if axis == AXIS_LEFT_STICK_X:
            return self._current_inputs[1]
        elif axis == AXIS_LEFT_STICK_Y:
            return self._current_inputs[2]

    def has_axis_value_changed(self, axis, threshold):
        """检测摇杆轴的值是否发生了有效移动"""
        """Check if joystick axis value has moved significantly"""
        if axis == AXIS_LEFT_STICK_X:
            return self._has_axis_value_changed_significantly(self._prev_inputs[1], self._current_inputs[1], threshold)
        elif axis == AXIS_LEFT_STICK_Y:
            return self._has_axis_value_changed_significantly(self._prev_inputs[2], self._current_inputs[2], threshold)
        else:
            raise Exception(f"Invalid axis: {axis}")

    def _has_axis_value_changed_significantly(self, previous_value: int, current_value: int, threshold: int):
        """内部方法：检测摇杆值是否发生了有效变化"""
        """Internal method: Check if axis value has changed significantly"""
        return (previous_value != current_value) and (current_value == 0 or current_value == 0xFF or abs(previous_value - current_value) >= threshold)

    def axis_values(self):
        """获取左右摇杆的当前值（X轴，Y轴）"""
        """Get current values of both joysticks (X axis, Y axis)"""
        return self._current_inputs[1], self._current_inputs[2]
