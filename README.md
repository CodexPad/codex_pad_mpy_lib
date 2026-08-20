# CodexPad MicroPython Lib

[中文](README.zh-CN.md)

## Overview

This library is the **MicroPython** for the **CodexPad** series controllers. It supports ESP32 series development boards in connecting to and reading the input status of all buttons and joysticks on a CodexPad controller via Bluetooth. For detailed information about CodexPad products, please refer to the product documentation below.

| CodexPad Model | Details |
| :--- | :--- |
| CodexPad-C10 | [Product Details](../../../codex_pad_c10/blob/main/README.md#codexpad-c10) |
| CodexPad-S10 | [Product Details](../../../codex_pad_s10/blob/main/README.md#codexpad-s10) |

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
| ESP32-P4 |
| Raspberry Pi Pico W |
| Raspberry Pi Pico 2 W |

## Features

- **Flexible Dual-Mode Connection**:

  - **Direct Connection via Bluetooth Device Address**: Quickly establish a stable connection with a specific controller using a known Bluetooth Device Address.

  - **Button Mask Scan Connection**: Connect without knowing the Bluetooth Device Address in advance. By scanning for and matching a specific combination of buttons held down on the target controller (defined as a "button mask" in your code), the library automatically connects to the device with the strongest signal (highest RSSI), enabling fast and flexible pairing.

- **Real-time Button Event Detection**: Reads the input status of all buttons in real time, distinguishing between **Pressed**, **Released**, and **Holding** events.

- **High-Precision Joystick Data**: Retrieves analog values for the X and Y axes of the left and right joysticks, ranging from 0 to 255, providing precise control input.

- **Adjustable Transmit Power**: Allows dynamic adjustment of the Bluetooth transmit power within a range of **-16 dBm to +6 dBm** based on the application scenario (e.g., distance, power requirements).

## Detailed Explanation of Button Mask Scan Connection

**Button Mask Scan Connection** is a distinctive feature of CodexPad, allowing the host to connect by scanning for and matching a specific combination of buttons held down on the device. This method establishes a physical "handshake" protocol between the device and the host, offering significant advantages in multi-device environments and flexible pairing scenarios.

### Design Intent and Advantages

1. **Preventing Accidental Connections and Interference**: When multiple connectable devices of the same type (e.g., multiple controllers) are nearby, while their unique **Bluetooth Device Address** can be used for precise connection, this typically requires "hardcoding" the address in the code. This approach binds the program to a specific device, lacking flexibility. By requiring the target device to hold a specific button combination while being discovered, a dynamic, condition-based connection rule is defined. Your connection code is not bound to any device's physical address; as long as a device satisfies this "handshake protocol" (holding the correct buttons), it will be connected. This effectively prevents the host from accidentally connecting to the wrong device among multiple devices, while enabling the convenience of **connect on press, with the ability to switch devices at any time**.

2. **Creating Exclusive Connection Conditions**: You can think of this button mask as a simple "password" or "connection token." It creates an exclusive connection channel between your application and the device, allowing only devices that meet this specific physical interaction condition (pressing the designated buttons) to join, enhancing the intentionality and control of the connection.

3. **Improving Code Flexibility, Supporting On-the-Fly Device Switching**: Unlike hardcoding a specific device's Bluetooth Device Address, the connection logic using a button mask is oriented towards a "condition" rather than a "specific device." This means your same set of connection code, without modification, can be used to connect to any controller that is discoverable and correctly triggers the preset button condition. This offers two major conveniences:

    - **No Need to Bind to a Specific Device**: You don't need to specify a controller's address in the code, nor maintain different connection configurations for different controllers.

    - **Connect on Press, Flexible Switching**: In practical use, you can pick up another controller at any time. As long as it is powered on and holding the correct button combination, your program can automatically connect to it, enabling seamless switching between different controllers.

### Working principle and operating steps

1. **Set the mask**: Define a **button mask** in your code and assign it to the relevant parameters of the connection function.

2. **Turn on the device**: Power on your controller to make it discoverable via Bluetooth (the controller’s indicator should flash slowly at this point).

3. **Execute connection**: Run your program. While the program is scanning, precisely press and hold all the buttons defined in your mask on the target controller.

4. **Automatic pairing**: When the program scans a device, it checks whether the button state exactly matches the preset mask (all specified buttons are pressed and no unspecified button is pressed). Once a match is found, the program automatically connects to the device with the strongest signal among matching devices.

> **⚠️ Important Warning**: The button mask MUST NEVER include the BUTTON_HOME (Home button). Pressing and holding the Home button triggers a system reset of the controller, which will directly interrupt the connection process and put the device into an unpredictable state.

### Example

The library provides full code implementation for this feature. Please refer to the examples and code in later sections.

## Usage Instructions

### Preparations

Before starting to program, complete the following preparations to ensure a smooth development process.

#### Familiarize Yourself with the Product Documentation

Read the CodexPad product manual in detail to fully understand the hardware features, familiarize yourself with the controller's button/joystick layout, function definitions, indicator light statuses, and power on/off operations.

#### Obtain and Record the Controller's Bluetooth Device Address (BD_ADDR)

> ⚠️ Important Note: The direct connection example in this library connects using the Bluetooth Device Address (BD_ADDR). When programming, you must explicitly specify your controller's Bluetooth Device Address (BD_ADDR) in the code.

Please refer to the method provided in the product manual to obtain your controller's **Bluetooth Device Address (BD_ADDR)**. It is typically in the format "`E4:66:E5:A2:24:5D`"(consisting of characters 0-9, A-F, with colons as half-width symbols). Record this information properly, as you will need to input your controller's actual **Bluetooth Device Address (BD_ADDR)** in the code later.

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

    **Download link**: [codex_pad_mpy_lib-x.x.x.zip](../../../codex_pad_mpy_lib/archive/refs/tags/v3.0.0.zip)

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
