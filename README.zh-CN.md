# CodexPad MicroPython Lib

[English](README.md)

## 概述

本库为**CodexPad**系列手柄提供的**MicroPython**库，支持ESP32系列开发板通过蓝牙连接并读取手柄的所有按键与摇杆输入状态。

## 支持的硬件平台

**理论支持范围**：本库理论上支持所有运行了内置标准**bluetooth**模块的**MicroPython**固件、且硬件本身具备 **低功耗蓝牙（BLE）** 功能的开发平台。您可以通过 [MicroPython官方下载页面（已筛选BLE功能）](https://micropython.org/download/?features=BLE)来查找和确认适合您设备的、支持蓝牙的官方固件。

下表列出了我们已测试可用的部分硬件平台：

| 支持的硬件平台 |
| :--- |
| ESP32 |
| ESP32-S3 |
| ESP32-C2 |
| ESP32-C3 |
| ESP32-C5 |
| ESP32-C6 |
| Raspberry Pi Pico W |
| Raspberry Pi Pico 2 W |

## 特性

- **灵活的双模式连接**：
  - **地址直连**：通过手柄的地址快速与指定手柄建立稳定连接。
  - **按键掩码连接**：通过扫描并匹配目标手柄上被按住的、由用户代码自定义的按键组合（即“按钮掩码”），自动连接信号最强（RSSI最大）的设备，实现快速、灵活的配对。
- **实时按键事件检测**：可实时读取所有按键的输入状态，并区分**按下**、**释放**和**按住**三种事件。
- **高精度摇杆数据**：获取左右摇杆X轴和Y轴的模拟量数值，范围从0至255，提供精准的控制输入。

## 使用说明

### 准备工作

在开始编程前，请完成以下准备工作，以确保开发过程顺利进行。

#### 熟悉产品文档

- 详细阅读手柄产品文档，全面了解硬件特性、熟悉手柄按键摇杆布局、功能定义、指示灯状态、地址获取的方法以及开关机操作等基本信息。

#### 开启手柄并进入待连接状态

- 将手柄开机，手柄开机后会自动处于蓝牙可被发现的**待连接状态**，此时手柄指示灯应呈现**慢闪状态（约每秒闪烁一次）**。

### 运行 MicroPython 环境

确保您的主机设备（如 ESP32）已烧录 **MicroPython 固件**，且其版本**不低于 `1.27.0`**。您可以在 REPL 中使用 `import sys; print(sys.version)` 命令来查看当前版本。

### 安装 **aioble** 依赖库

#### 平台差异与验证

本库依赖aioble库来实现蓝牙通信。根据您所使用的硬件平台，aioble库的提供方式可能不同：

- **ESP32 系列**：绝大多数 MicroPython 固件不预装​ **aioble** 库，您必须通过下方提供的方法进行安装。

- **Raspberry Pi Pico W / Pico 2 W**：官方 MicroPython 固件通常已预装​ **aioble** 库。您可以直接尝试导入，无需执行安装步骤。

在开始安装前，建议在 MicroPython 的 REPL 环境中，输入并执行以下单行命令进行验证：

```python
__import__('aioble'); print('aioble library is ready')
```

**如果控制台打印出 aioble library is ready**：表明aioble库已存在，您可以跳过后续的安装步骤。

**如果提示 ImportError: no module named 'aioble'**：表明库未找到，请根据您的设备是否已连接网络，选择以下任一方法。

#### 方法一：在设备REPL中通过mip安装（需要硬件设备网络）

> **⚠️重要提示**：此方法要求您的MicroPython设备本身（如ESP32）必须能够连接Wi-Fi并访问互联网。mip安装器会在设备端直接下载库文件。如果您的设备不具备网络功能（例如某些仅支持BLE的定制开发板），此方法将无法使用，请改用下方的“方法二”。

1. **确保网络连接**：请务必确保您的设备可以正常连接到互联网。您可能需要提前准备并测试好连接 Wi-Fi 的代码。

2. **执行安装代码**：在 MicroPython REPL 中，依次输入并执行以下命令。您也可以将这段代码保存为`main.py`文件，通过 Thonny 等工具上传到设备并运行，效果相同。

    ```python
    import network
    import time

    # 连接到您的Wi-Fi网络
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False) # 先关闭，确保状态重置
    wlan.active(True)
    print("Connecting")
    wlan.connect("your_ssid", "your_password")  # 请替换为实际的Wi-Fi名称和密码

    # 等待连接成功
    while not wlan.isconnected():
        time.sleep(0.5)

    print("WLAN connected")

    # 安装 aioble 库
    import mip
    mip.install("aioble")
    ```

3. **安装结果**：安装成功后，您将在 REPL 中看到类似以下的输出，表明库文件已成功拷贝到设备的 /lib目录下：

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

**重要提示**：

- **网络依赖**：此方法完全依赖设备本机的网络连接。如果安装失败，请首先检查设备的Wi-Fi连接是否正常，并确保其可以访问`micropython.org`的包索引服务。

- **重试机制**：若安装过程中因网络问题中断，您可以重新执行`mip.install("aioble")`命令进行重试。

#### 方法二：通过 Thonny IDE 的包管理器安装

1. 使用 Thonny IDE 连接您的主机设备。

2. 点击顶部菜单栏的 “工具(Tools)”​ → “管理包(Manage packages)”。

3. 在打开的对话框中，搜索**aioble**并进行安装。

### 安装 CodexPad 库

1. **下载库文件**

    **下载链接**：[codex_pad_mpy_lib-x.x.x.zip](../../../codex_pad_mpy_lib/archive/refs/tags/v4.0.0.zip)

2. **解压文件**

    将下载的 `codex_pad_mpy_lib-x.x.x.zip` 压缩包解压到本地文件夹。

3. **上传库文件**

    在解压后的文件夹中，找到 `codex_pad.py` 文件。

    使用 **Thonny**、**ampy** 或 **rshell** 等工具，将该文件上传到您的 MicroPython 设备文件系统的 **根目录 (`/`)** 或 **`/lib/`** 目录下。

## 示例说明

示例代码中包含详细的注释说明，建议直接查阅代码文件以获取最完整的信息。以下简要介绍各示例的核心功能与预期行为，助您快速入门。

### 基础轮询示例 (`basic_polling`)

- **文件位置**：[examples/basic_polling/main.py](examples/basic_polling/main.py)
- **示例说明**：通过Bluetooth Device Address与CodexPad蓝牙连接，实时查询、打印其所有按钮状态与摇杆数值。

### 输入状态检测示例 (`inputs_detection`)

- **文件位置**：[examples/inputs_detection/main.py](examples/inputs_detection/main.py)
- **示例说明**：通过Bluetooth Device Address与CodexPad蓝牙连接，检测到按钮状态与摇杆数值变化后打印。

### 扫描连接示例 (`scan_and_connect`)

- **文件位置**：[examples/scan_and_connect/main.py](examples/scan_and_connect/main.py)
- **示例说明**：通过匹配特定的自定义的**按键**或者**按键组合**来扫描并自动连接附近的 CodexPad 设备，检测摇杆和按键变化并打印。
- **操作步骤**：代码启动后进入扫描连接状态，手柄开机后蓝灯闪烁，此时按住手柄上你代码中指定的按键掩码（按键组合）直到主机连接到手柄为止，之后正常操作手柄观察控制台的日志输出。
- **重要提示**：设置按钮掩码时，**请勿单独使用 `Home` 键**。长按 `Home` 键会导致手柄关机，从而中断连接。如确需使用 `Home` 键，请务必采用组合按键（如 `Home` + `Cross`）。

## 按键掩码连接功能详解

详情链接：[按键掩码连接功能详解](../../../codex_pad_guide/blob/main/button_mask_connection_explained.zh-CN.md#按键掩码连接功能详解)

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
