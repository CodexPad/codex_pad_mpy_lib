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

- **蓝牙Bluetooth Device Address连接**：通过已知的CodexPad手柄蓝牙Bluetooth Device Address，快速建立与指定CodexPad手柄的稳定连接。
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

确保您的主机设备（如 ESP32）已烧录 **MicroPython 固件**，且其版本**不低于 `1.21.0`**。您可以在 REPL 中使用 `import sys; print(sys.version)` 命令来查看当前版本。

### 安装 CodexPad 库

1. 从本仓库的 `lib/` 目录下获取 `codex_pad.mpy` 库文件。
2. 使用 **Thonny**、**ampy** 或 **rshell** 等工具，将该库文件上传到您主机设备的**文件系统根目录（`/`）** 下。

## 示例说明

示例代码中包含详细的注释说明，建议直接查阅代码文件以获取最完整的信息。以下简要介绍各示例的核心功能与预期行为，助您快速入门。

### 基础轮询示例 (`basic_polling`)

- **文件位置**：[examples/basic_polling/main.py](examples/basic_polling/main.py)
- **示例说明**：通过Bluetooth Device Address与CodexPad蓝牙连接，实时查询、打印其所有按钮状态与摇杆数值。

### 输入状态检测示例 (`inputs_detection`)

- **文件位置**：[examples/inputs_detection/main.py](examples/inputs_detection/main.py)
- **示例说明**：通过Bluetooth Device Address与CodexPad蓝牙连接，检测到按钮状态与摇杆数值变化后打印。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
