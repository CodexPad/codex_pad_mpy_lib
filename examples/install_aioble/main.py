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