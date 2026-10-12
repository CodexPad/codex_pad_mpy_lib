# CodexPad MicroPython Lib

[中文](README.zh-CN.md)

## Overview

This library is the **MicroPython** for the **CodexPad** series controllers. It supports ESP32 series development boards in connecting to and reading the input status of all buttons and joysticks on a CodexPad controller via Bluetooth.

## Supported Hardware Platforms

**Theoretical Support Scope**: This library theoretically supports all development platform running **MicroPython** firmware with the built-in standard **bluetooth** module, provided the hardware itself has **Bluetooth Low Energy (BLE)** capability. You can check the [official MicroPython download page (filtered for BLE)](https://micropython.org/download/?features=BLE) to find suitable firmware for your device.

The following table lists the available hardware platforms that we have tested:

| Supported Hardware Platforms |
| :--- |
| ESP32 |
| ESP32-S3 |
| ESP32-C2 |
| ESP32-C3 |
| ESP32-C5 |
| ESP32-C6 |
| Raspberry Pi Pico W |
| Raspberry Pi Pico 2 W |

## Features

- **Flexible Dual-Mode Connection**:
  - **Direct Connection via Address**: Quickly establish a stable connection with a specific controller using a known Bluetooth Device Address.
  - **Button Mask Connection**: By scanning for and matching a specific combination of buttons held down on the target controller (defined as a "button mask" in your code), the library automatically connects to the device with the strongest signal (highest RSSI), enabling fast and flexible pairing.
- **Real-time Button Event Detection**: Reads the input status of all buttons in real time, distinguishing between **Pressed**, **Released**, and **Holding** events.
- **High-Precision Joystick Data**: Retrieves analog values for the X and Y axes of the left and right joysticks, ranging from 0 to 255, providing precise control input.

## Usage Instructions

### Preparations

Before starting to program, complete the following preparations to ensure a smooth development process.

#### Familiarize Yourself with the Product Documentation

Read the CodexPad product manual in detail to fully understand the hardware features, familiarize yourself with the controller's button/joystick layout, function definitions, indicator light statuses, obtaining address, and power on/off operations.

#### Power On the Controller and Enter Pairing Mode

Power on the controller. After powering on, the controller will automatically enter the **pairing mode** where it is discoverable via Bluetooth. At this time, the controller's indicator light should be in a **slow blinking state (approximately once per second)**.

### Running the MicroPython Environment

Ensure that your host device (e.g. ESP32) has been burned with **MicroPython firmware** and its version is **not less than 1.27.0**. You can check the current version in the REPL by using the command `import sys; print(sys.version)`.

### Installing the **aioble** Dependency

#### Platform Differences and Verification

This library relies on the `aioble` library for Bluetooth communication. The availability of the `aioble` library may differ depending on your hardware platform:

- **ESP32 series**: Most MicroPython firmwares do **not** pre-install the **aioble** library. You must install it using one of the methods below.

- **Raspberry Pi Pico W / Pico 2 W**: The official MicroPython firmware usually comes with the **aioble** library pre-installed. You can try importing it directly without performing the installation steps.

Before starting the installation, we recommend verifying by entering and executing the following one-liner in the MicroPython REPL:

```python
__import__('aioble'); print('aioble library is ready')
```

**If the console prints out "aioble library is ready"**: This indicates the aioble library already exists, and you can skip the subsequent installation steps.

**If you see "ImportError: no module named 'aioble'"**: This means the library is not found. Depending on whether your device has network access, choose one of the following methods.

#### Method 1: Install via mip in the device REPL (requires device network connection)

> **⚠️ Important**: This method requires that your MicroPython device (e.g., ESP32) can connect to Wi-Fi and access the internet. The mip installer downloads the library files directly on the device. If your device does not have network capabilities (e.g., some custom BLE-only development boards), this method will not work. Please use "Method 2" below instead.

1. **Ensure network connection**: Make sure your device can properly connect to the internet. You may need to prepare and test the Wi-Fi connection code beforehand.

2. **Execute the installation code**: In the MicroPython REPL, enter and execute the following commands one by one. You can also save this code as a `main.py` file, upload it to the device using tools like Thonny, and run it – the effect is the same.

    ```python
    import network
    import time

    # Connect to your Wi-Fi network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False) # Deactivate first to reset the state
    wlan.active(True)
    print("Connecting")
    wlan.connect("your_ssid", "your_password")  # Replace with your actual Wi-Fi name and password

    # Wait for the connection to succeed
    while not wlan.isconnected():
        time.sleep(0.5)

    print("WLAN connected")

    # Install the aioble library
    import mip
    mip.install("aioble")
    ```

3. **Installation result**: After a successful installation, you will see output similar to the following in the REPL, indicating that the library files have been copied to the device's /lib directory:

    ```log
    Connecting
    WLAN connected
    Installing aioble (latest) from https://micropython.org/pi/v2 to /lib
    Copying: /lib/aioble/__init__.mpy
    Copying: /lib/aioble/core.mpy
    Copying: /lib/aioble/device.mpy
    Copying: /lib/aioble/peripheral.mpy
    Copying: /lib/aioble/server.mpy
    Copying: /lib/aioble/central.mpy
    Copying: /lib/aioble/client.mpy
    Copying: /lib/aioble/l2cap.mpy
    Copying: /lib/aioble/security.mpy
    Done
    ```

**Important Notice**:

- **Network Dependency**: This method relies entirely on the local network connection of the device. If the installation fails, please first check whether the device's WiFi connection  is working and ensure it can access the package index service at `micropython.org`.

- **retry mechanism**: If the installation is interrupted due to network issues, you can re-execute the ` mip.install ("aioble") ` command to retry.

#### Method 2: Install via Thonny IDE's package manager

1. Use Thonny IDE to connect to your host device.

2. Click on "Tools" → "Manage packages" in the top menu bar.

3. In the dialog that opens, search for **aioble** and install it.

### Install the CodexPad library

1. **Download the library file**

    **Download link**: [codex_pad_mpy_lib-x.x.x.zip](../../../codex_pad_mpy_lib/archive/refs/tags/v4.0.0.zip)

2. **Extract the files**

    Extract the downloaded `codex_pad_mpy_lib-x.x.x.zip` archive to a local folder.

3. **Upload the library file**

    Inside the extracted folder, locate the `codex_pad.py` file.

    Use tools like **Thonny**, **ampy**, or **rshell** to upload this file to the **root directory (`/`)** or the **`/lib/`** directory of your MicroPython device's filesystem.

## Example Descriptions

The example code contains detailed comments. It is recommended to read the code files directly for the most complete information. Below is a brief introduction to the core functionality and expected behavior of each example to help you get started quickly.

### Basic Polling Example (`basic_polling`)

- **File location**: [examples/basic_polling/main.py](examples/basic_polling/main.py)
- **Description**: Connects to CodexPad via Bluetooth Device Address, polls and prints all button states and joystick values in real time.

### Input State Detection Example (`inputs_detection`)

- **File location**: [examples/inputs_detection/main.py](examples/inputs_detection/main.py)
- **Description**: Connects to CodexPad via Bluetooth Device Address, detects changes in button states and joystick values, and prints them.

### Scan and Connect Example (`scan_and_connect`)

- **File location**: [examples/scan_and_connect/main.py](examples/scan_and_connect/main.py)
- **Description**: Scans for and automatically connects to a nearby CodexPad device by matching a specific custom **button** or **button combination**, then detects joystick and button changes and prints them.
- **Steps**: After the code starts, it enters the scan-and-connect state. When the gamepad is powered on and the blue light flashes, press and hold the button mask (button combination) specified in your code until the host connects to the gamepad. Afterwards, operate the gamepad normally and observe the console log output.
- **Important**: When setting the button mask, **do not use the `Home` button alone**. Long-pressing the `Home` button will cause the gamepad to power off, thereby interrupting the connection. If you do need to use the `Home` button, be sure to use it in a combination (e.g., `Home` + `Cross`).

## Button Mask Connection Explained

Details: [Button Mask Connection Explained](../../../codex_pad_guide/blob/main/button_mask_connection_explained.md#button-mask-connection-explained)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
