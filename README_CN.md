# 🎮 CodexPad MicroPython 库

[English](README.md)

## 概述

本库为**CodexPad**系列手柄提供的**MicroPython**库，支持ESP32系列开发板通过蓝牙连接并读取CodexPad手柄的所有按键与摇杆输入状态。关于 CodexPad 产品的详细信息，请查阅以下产品文档。

| CodexPad型号 | 链接 |
| :--- | :--- |
| CodexPad-C10 | <https://github.com/CodexPad/codex_pad_c10> |
| CodexPad-S10 | <https://github.com/CodexPad/codex_pad_s10> |

## 支持的硬件平台

**理论支持范围**：本库理论上支持所有**具备蓝牙功能**、并**运行了支持标准BLE接口的MicroPython固件**的硬件平台。您可以通过 [MicroPython官方下载页面（已筛选BLE功能）](https://micropython.org/download/?features=BLE)来查找和确认适合您设备的、支持蓝牙的官方固件。

下表列出了我们已测试可用的部分硬件平台：

| 支持的硬件平台 |
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

## 特性

- **灵活的双模式连接**：

  - **Bluetooth Device Address直连**：通过已知的**Bluetooth Device Address**，快速与指定手柄建立稳定连接。

  - **按键掩码扫描连接**：无需提前知道**Bluetooth Device Address**。通过扫描并匹配目标手柄上被按住的、由用户代码自定义的按键组合（即“按钮掩码”），自动连接信号最强（RSSI最大）的设备，实现快速、灵活的配对。

- **实时按键事件检测**：可实时读取所有按键的输入状态，并区分**按下**、**释放**和**长按**三种事件。

- **高精度摇杆数据**：获取左右摇杆X轴和Y轴的模拟量数值，范围从0至255，提供精准的控制输入。

- **可调发射功率**：允许根据实际应用场景（如距离、功耗需求），在-16 dBm至+6 dBm范围内动态调整蓝牙发射功率。

## 按键掩码扫描连接功能详解

**按键掩码扫描连接**是CodexPad的一项特色功能，允许主机通过扫描并匹配设备上被按住的特定按键组合来进行连接。这种方式通过在设备与主机间建立一个物理“握手”协议，从而在多设备环境和灵活配对场景下具有显著优势。

### 设计意图与优势

1. **防止意外连接与干扰**：当周围存在多个可连接的同类设备（例如多个手柄）时，虽然通过其唯一的**Bluetooth Device Address**可以进行精确连接，但这通常需要在代码中“硬编码”该地址。这种方式将程序与特定设备绑定，缺乏灵活性。通过要求目标设备在被发现时必须同时按住一个特定的按键组合，相当于定义了一个动态的、基于条件的连接规则。您的连接代码无需绑定任何设备的物理地址，只要设备满足此“握手协议”（按住正确按键），就会被连接。这既有效避免了主机在多个设备中意外连接到非目标设备，又实现了**即按即连，设备可随时切换**的便捷性。

2. **构建专属连接条件**：你可以将此按键掩码视为一个简单的“密码”或“连接令牌”。它为你的应用程序和设备间构建了一个专属的连接通道，只有满足此特定物理交互条件（按下指定按键）的设备才能加入，增强了连接的意图性和可控性。

3. **提升代码灵活性，支持设备随时切换**：与在代码中硬编码特定设备的Bluetooth Device Address不同，使用按键掩码的连接逻辑是面向“条件”而非“特定设备”的。这意味着你的同一套连接代码，无需修改，即可用于连接任何处于可发现状态、并正确触发了预设按键条件的手柄。这带来了两大便利：

    - **无需绑定特定设备**：你无需在代码中指定某个手柄的地址，也无需为不同的手柄维护不同的连接配置。

    - **即按即连，灵活切换**：在实际使用中，你可以随时拿起另一个手柄，只要它开机并按住正确的按键组合，你的程序就能自动连接到它，实现了在不同手柄间的无缝切换。

### 工作原理与操作步骤

1. **设置掩码**：在您的代码中定义一个**按钮掩码**，并将其赋值给连接函数的相关参数。

2. **开启设备**：开启您的手柄设备，使其进入蓝牙可被发现的待连接状态（此时手柄指示灯应慢闪）。

3. **执行连接**：运行您的程序。当程序开始扫描时，在目标手柄上，精确地同时按住您在掩码中定义的所有按键。

4. **自动配对**：程序扫描到设备后，会检查其按键状态是否与预设的掩码完全匹配（即按住了所有指定按键，且未按下任何未指定的按键）。一旦匹配成功，程序便会自动与信号最强的匹配设备建立连接。

> **⚠️重要警告**：按钮掩码中绝对禁止包含 BUTTON_HOME(Home键)。因为长按 Home 键会触发手柄系统重启，这将直接导致连接过程中断，并使设备进入不可预期的状态。

### 示例

本库为此功能提供了完整的代码实现，请参考后续章节中的示例说明与代码。

## 使用说明

### 准备工作

在开始编程前，请完成以下准备工作，以确保开发过程顺利进行。

#### 熟悉产品文档

- 详细阅读 CodexPad 产品手册，全面了解硬件特性、熟悉手柄按键摇杆布局、功能定义、指示灯状态以及开关机操作等基本信息。

#### 获取并记录手柄**Bluetooth Device Address(BD_ADDR)**

> **⚠️重要提示**：本库直连的示例是通过 **Bluetooth Device Address(BD_ADDR)** 进行连接。**编程时，必须在代码明确指定您手柄的Bluetooth Device Address(BD_ADDR)。**

请参考产品手册中提供的方法，获取您手柄的**Bluetooth Device Address(BD_ADDR)**。其格式通常为 `"E4:66:E5:A2:24:5D"`（由0-9、A-F的字符组成，冒号为半角）。请妥善记录此信息，后续需要在代码为您自己手柄的实际**Bluetooth Device Address(BD_ADDR)**。

#### 开启手柄并进入待连接状态

- 将手柄开机，手柄开机后会自动处于蓝牙可被发现的**待连接状态**，此时手柄指示灯应呈现**慢闪状态（约每秒闪烁一次）**。

### 运行 MicroPython 环境

确保您的主机设备（如 ESP32）已烧录 **MicroPython 固件**，且其版本**不低于 `1.27.0`**。您可以在 REPL 中使用 `import sys; print(sys.version)` 命令来查看当前版本。

### 安装 **aioble** 依赖库

#### 平台差异与验证

本库依赖aioble库来实现蓝牙通信。根据您所使用的硬件平台，aioble库的提供方式可能不同：

**ESP32 系列**：绝大多数 MicroPython 固件不预装​ **aioble** 库，您必须通过下方提供的方法进行安装。

**Raspberry Pi Pico W / Pico 2 W**：官方 MicroPython 固件通常已预装​ **aioble** 库。您可以直接尝试导入，无需执行安装步骤。

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
- **示例说明**：通过匹配特定的自定义的**按键**或者**按键组合**来扫描并自动连接附近的 CodexPad 设备，检测摇杆和按键变化并打印。
- **操作步骤**：代码启动后进入扫描连接状态，此时按住手柄上你代码中指定的按键掩码（按键组合）直到主机连接到手柄为止，之后正常操作手柄观察控制台的日志输出。
- **重要警告**：按钮掩码中**绝对禁止**包含 `Home` 键，因为长按 Home 键会导致手柄重启，从而中断连接。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
