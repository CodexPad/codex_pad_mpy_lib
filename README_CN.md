# 🎮 CodexPad MicroPython 库

[English](README.md)

## 概述

本库为**CodexPad**系列手柄提供的**MicroPython**库，支持ESP32系列开发板通过蓝牙连接并读取CodexPad手柄的所有按键与摇杆输入状态。关于 CodexPad 产品的详细信息，请查阅以下产品文档。

| CodexPad型号 | 链接 |
| :--- | :--- |
| CodexPad-C10 | <https://github.com/CodexPad/codex_pad_c10> |
| CodexPad-S10 | <https://github.com/CodexPad/codex_pad_s10> |

## 支持的硬件平台

| 支持的硬件平台 |
| :--- |
| ESP32 |
| ESP32-S2 |
| ESP32-S3 |
| ESP32-C3 |
| ESP32-C5 |
| ESP32-C6 |
| ESP32-H2 |
| ESP32-P4 |

## 特性

- **灵活的双模式连接**：

  - **Bluetooth Device Address直连**：通过已知的**Bluetooth Device Address**，快速与指定手柄建立稳定连接。

  - **按键掩码扫描连接**：无需提前知道**Bluetooth Device Address**。通过扫描并匹配目标手柄上被按住的、由用户代码自定义的按键组合（即“按钮掩码”），自动连接信号最强（RSSI最大）的设备，实现快速、灵活的配对。

- **实时按键事件检测**：可实时读取所有按键的输入状态，并区分**按下**、**释放**和**长按**三种事件。

- **高精度摇杆数据**：获取左右摇杆X轴和Y轴的模拟量数值，范围从0至255，提供精准的控制输入。

- **可调发射功率**：允许根据实际应用场景（如距离、功耗需求），在-16 dBm至+6 dBm范围内动态调整蓝牙发射功率。

## 使用说明

### 准备工作

在开始编程前，请完成以下准备工作，以确保开发过程顺利进行。

#### 熟悉产品文档

- 详细阅读 CodexPad 产品手册，全面了解硬件特性、熟悉手柄按键摇杆布局、功能定义、指示灯状态以及开关机操作等基本信息。

#### 获取并记录手柄**Bluetooth Device Address(BD_ADDR)**

> **⚠️ 重要提示**：本库直连的示例是通过 **Bluetooth Device Address(BD_ADDR)** 进行连接。**编程时，必须在代码明确指定您手柄的Bluetooth Device Address(BD_ADDR)。**

请参考产品手册中提供的方法，获取您手柄的**Bluetooth Device Address(BD_ADDR)**。其格式通常为 `"E4:66:E5:A2:24:5D"`（由0-9、A-F的字符组成，冒号为半角）。请妥善记录此信息，后续需要在代码为您自己手柄的实际**Bluetooth Device Address(BD_ADDR)**。

#### 开启手柄并进入待连接状态

- 将手柄开机，手柄开机后会自动处于蓝牙可被发现的**待连接状态**，此时手柄指示灯应呈现**慢闪状态（约每秒闪烁一次）**。

### 运行 MicroPython 环境

确保您的主机设备（如 ESP32）已烧录 **MicroPython 固件**，且其版本**不低于 `1.27.0`**。您可以在 REPL 中使用 `import sys; print(sys.version)` 命令来查看当前版本。

### 安装 **aioble** 依赖库

本库依赖 aioble库来实现蓝牙通信功能。在安装本库前，请确保您的主机设备（ESP32）已连接网络，并先行安装 aioble库。您可以选择以下任一方法进行安装：

#### 方法一：在设备REPL中通过mip安装

此方法通过在 MicroPython 的交互式环境（REPL）中直接执行 Python 代码来完成安装。

1. **确保网络连接**：请务必确保您的设备可以正常连接到互联网。您可能需要提前准备并测试好连接 Wi-Fi 的代码。

2. **执行安装代码**：在 MicroPython REPL 中，依次输入并执行以下命令。您也可以将这段代码保存为 main.py文件，通过 Thonny 等工具上传到设备并运行，效果相同。

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

- **网络依赖**：此方法完全依赖网络。如果安装失败，请首先检查设备的 Wi-Fi 连接是否正常，并确保其可以访问 `micropython.org` 的包索引服务。

- **重试机制**：若安装过程中因网络问题中断，您可以重新执行`mip.install("aioble")`命令进行重试。

#### 方法二：通过 Thonny IDE 的包管理器安装

1. 使用 Thonny IDE 连接您的主机设备。

2. 点击顶部菜单栏的 “工具(Tools)”​ → “管理包(Manage packages)”。

3. 在打开的对话框中，搜索**aioble**并进行安装。

### 安装 CodexPad 库

1. 从本仓库的 `lib/` 目录下获取 `codex_pad.py` 库文件。

2. 使用 **Thonny**、**ampy** 或 **rshell** 等工具，将该库文件`codex_pad.py`上传到您主机设备的**文件系统根目录（`/`）** 下，或者 **`/lib/`** 目录下。

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
- **核心功能**：通过匹配特定的自定义的**按键**或者**按键组合**来扫描并自动连接附近的 CodexPad 设备，检测摇杆和按键变化并打印。
- **重要警告**：按钮掩码中**绝对禁止**包含 `Home` 键，因为长按 Home 键会导致手柄重启，从而中断连接。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
