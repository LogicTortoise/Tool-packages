# 环境配置指南

## 硬件要求

- **Android 模拟器**: BlueStacks / 雷电 / 夜神等
- **分辨率**: 720x1280（竖屏）- 必须严格遵守
- **DPI**: 240 或 320

## 软件要求

- Python 3.8+
- 同花顺 APP (版本 11.46.04, 包名: com.hexin.plat.android)
- ADB 工具

## 安装步骤

### 1. 安装 Python 依赖

```bash
cd /Users/Hht/agent/skills/thstrader/scripts
pip install -r requirements.txt
```

依赖包括:
- uiautomator2 - Android UI 自动化
- easyocr - OCR 文字识别
- Pillow - 图像处理

### 2. 配置 BlueStacks 模拟器

1. 打开 BlueStacks 设置
2. **显示** → **分辨率**: 自定义 720x1280
3. **显示** → **DPI**: 240
4. **重启模拟器**

### 3. 连接 ADB

```bash
# 连接 BlueStacks
adb connect 127.0.0.1:5565

# 验证连接
adb devices
```

预期输出:
```
List of devices attached
127.0.0.1:5565    device
```

### 4. 安装同花顺 APP

下载同花顺 APK (版本 11.46.04):

```bash
adb -s 127.0.0.1:5565 install tonghuashun.apk
```

### 5. 配置同花顺

1. 启动同花顺 APP
2. 登录账号
3. 进入"模拟炒股"功能
4. 确保模拟炒股可以正常使用

## 验证安装

运行快速测试:

```bash
python trader.py balance --device 127.0.0.1:5565
```

如果成功，应该看到账户余额信息。

## 重要提示

⚠️ **分辨率必须是 720x1280**，否则坐标定位会失败
⚠️ **DPI 建议 240 或 320**
⚠️ **仅支持同花顺版本 11.46.04**
