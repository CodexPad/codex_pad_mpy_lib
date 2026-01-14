# 🎮 CodexPad MicroPython Lib

[中文](README_CN.md)

## Project Introduction

CodexPad MicroPython Library is a MicroPython driver library for CodexPad. CodexPad is a self-developed Bluetooth Low Energy (BLE) gamepad specifically designed for IoT devices and embedded systems.

This library supports using CodexPad on ESP32/ESP32-S3 and all MicroPython platforms with BLE support, providing simple and easy-to-use APIs to read button states and joystick data.

## Features

- ✅ Real-time State Detection​ - Provides state detection for pressed, released, and holding states
- ✅ Debounce Processing​ - Intelligently filters minor joystick jitter to ensure stable data
- ✅ Configurable Power​ - Supports adjusting BLE transmission power to balance range and power consumption
- ✅ Multi-platform Compatibility​ - Supports ESP32, ESP32-S series, and all MicroPython platforms with BLE support
- ✅ Complete API​ - Supports all button and joystick functions

## Hardware Requirements

### Supported Main Control Chips

- ESP32 series
- ESP32-S2/S3 series
- Any MicroPython platform with BLE support

### Required Hardware

- gamepad: CodexPad
- MicroPython development board with BLE support
- USB cable
- Optional: External antenna (for extended communication range)

## MicroPython Version Requirement

This library requires MicroPython firmware version `1.21.0` or above. Please ensure your host device is running a compatible MicroPython version.

## 🚀 Quick Start

### Prerequisites

#### Get CodexPad MAC Address

*Important: You need to obtain the MAC address of your gamepad before use*

Different models of gamepad may have different methods to obtain the MAC address. Please refer to the product documentation of your specific gamepad.

Product Documentation link: [CodexPad Product Documentation]()

After obtaining the MAC address, you will need it for device connection.

#### Run MicroPython Environment

*Host device must run MicroPython firmware*

Before using this library, ensure your host device (such as ESP32) has been flashed with MicroPython firmware and is running normally.

#### Start CodexPad

Start the gamepad and put it in pairing mode. The signal light on the gamepad will blink slowly (approximately 1 second on/off), indicating it's waiting for host connection.

### Install Library Files

- Use tools like Thonny, ampy, or rshell
- Upload files `lib/codex_pad.mpy` to the **root directory** of your device

### Configure and Upload Example Code

- Select the example code file you want to upload (located in `examples/` directory)

- *Important: Modify MAC address configuration*

    ```python
    # Replace the following address with your gamepad's actual MAC address
    codex_pad_obj.connect("E4:66:E5:A2:24:5D") # Replace with your gamepad's MAC address
    ```

- Use development tools to upload the file to the device `root` directory

- Restart the device to run automatically, the device will automatically connect to the gamepad

- After successful connection, the gamepad indicator light will stay on

- Operate the gamepad and observe the device serial output to view button and joystick information

## 📋Example Code Description

The example code contains detailed comments. You can directly view them, and detailed code explanations are not repeated here.

### Basic Polling Example

- **Location**: [examples/basic_polling/main.py](examples/basic_polling/main.py)
- **Use Case**: Applications requiring real-time control, such as robot control, real-time games, etc.
- **Features**: Simple and direct, suitable for beginners

### Input State Detection Example

- **Location**: [examples/state_detection/main.py](examples/state_detection/main.py)
- **Use Case**: Event-driven applications, such as menu navigation, state switching, etc.
- **Features**: Reactive programming, reducing unnecessary polling

## 🔧 Troubleshooting

### Common Issues

#### Q: How to get CodexPad MAC address?

A: Please refer to the product documentation of your specific CodexPad. Different CodexPad models may have different methods to obtain the MAC address.

#### Q: Connection failed

A: Check the following points:

- Ensure the gamepad is started and in pairing mode (indicator blinking slowly)
- Confirm the MAC address is correct
- Check if devices are within effective range

#### Q: No data response

A: Check the following points:

- Confirm the gamepad is successfully connected (indicator light stays on)
- Check if the update() method is correctly called in the code
- Check serial output for any error messages

#### Q: Response delay

A: Check the following points:

- Ensure there are no unnecessary delays in the main loop
- The update() method needs to be called frequently

## 📄 License

This project uses the MIT License - see [LICENSE](LICENSE) for details.

---

**CodexPad - Making Embedded Development Easier**
