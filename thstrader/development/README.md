# THSTrader-skill

新版同花顺模拟炒股自动化交易工具（适配版本 11.46.04）

基于 [THSTrader](https://github.com/nladuo/THSTrader) 复刻，适配新版同花顺 UI。

## 功能特性

### 核心功能
- ✅ **获取账户余额** - 查询总资产、可用资金、浮动盈亏等
- ✅ **获取持仓列表** - 查看当前持有的所有股票及数量
- ✅ **买入股票** - 自动化买入流程，支持价格和数量参数
- ✅ **卖出股票** - 自动化卖出流程
- ✅ **获取可撤单列表** - 查看所有待成交的委托
- ✅ **撤单** - 取消指定的委托订单

### 自选股管理 🆕
- ✅ **添加自选股** - 输入中文名称，按拼音首字母搜索并添加
- ✅ **移除自选股** - 从自选中移除指定股票
- ✅ **获取股票代码** - 从自选区查询股票代码
- ✅ **从自选区买入** - 直接使用股票名称买入（无需代码）
- ✅ **从自选区卖出** - 直接使用股票名称卖出（无需代码）

### 辅助功能
- 📸 **自动截图** - 每次交易自动保存截图记录
- 🔍 **OCR 识别** - 使用 EasyOCR 识别持仓和撤单信息
- 🛡️ **二次确认** - 买入/卖出前自动验证订单信息
- 🔤 **拼音搜索** - 支持中文股票名称拼音首字母快速搜索

## 环境要求

### 硬件环境
- Android 模拟器（BlueStacks / 雷电 / 夜神等）
- 分辨率：720x1280（竖屏）
- DPI：240 或 320

### 软件环境
- Python 3.8+
- 同花顺 APP（版本 11.46.04，包名：com.hexin.plat.android）
- ADB 工具

## 安装步骤

### 1. 克隆项目

```bash
cd /Users/Hht/Documents/10.github
git clone <repository-url> THSTrader-skill
cd THSTrader-skill
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置模拟器

#### BlueStacks 配置
1. 打开 BlueStacks 设置
2. 显示 → 分辨率：自定义 720x1280
3. 显示 → DPI：240
4. 重启模拟器

#### ADB 连接
```bash
# 连接 BlueStacks
adb connect 127.0.0.1:5565

# 验证连接
adb devices
```

### 4. 安装同花顺

下载并安装同花顺 APP（版本 11.46.04）：
```bash
adb -s 127.0.0.1:5565 install tonghuashun.apk
```

### 5. 配置同花顺
1. 启动同花顺 APP
2. 登录账号
3. 进入"模拟炒股"功能
4. 确保模拟炒股可以正常使用

## 使用方法

### 命令行界面

```bash
# 查看帮助
python trader.py --help

# 获取账户余额
python trader.py balance

# 获取持仓列表
python trader.py position

# 买入股票（股票代码、数量、价格）
python trader.py buy --code 002415 --amount 1000 --price 10.0

# 卖出股票
python trader.py sell --code 002415 --amount 500 --price 11.0

# 查看可撤单列表
python trader.py withdrawals

# 撤单
python trader.py cancel --name 海康威视 --type 买入 --amount 1000 --price 10.0

# 添加自选股
python trader.py add-favorite --name 海康威视

# 移除自选股
python trader.py remove-favorite --name 海康威视

# 获取自选股代码
python trader.py get-code --name 海康威视

# 从自选区买入（无需股票代码）
python trader.py buy-favorite --name 海康威视 --amount 1000 --price 31.5

# 从自选区卖出（无需股票代码）
python trader.py sell-favorite --name 海康威视 --amount 500 --price 32.0

# 指定设备
python trader.py balance --device 127.0.0.1:5565

# JSON 格式输出
python trader.py balance --json
```

### Python API

```python
from ths import THSTrader

# 初始化
trader = THSTrader("127.0.0.1:5565")

# 获取余额
balance = trader.get_balance()
print(balance)
# {'总资产': '200,000.00', '可用': '180,000.00', ...}

# 获取持仓
positions = trader.get_position()
for pos in positions:
    print(f"{pos['股票名称']}: {pos['股票余额']}股")

# 买入股票
result = trader.buy("002415", 1000, 10.0)
if result['success']:
    print(f"买入成功: {result['msg']}")

# 卖出股票
result = trader.sell("002415", 500, 11.0)
if result['success']:
    print(f"卖出成功: {result['msg']}")

# 获取可撤单列表
withdrawals = trader.get_avail_withdrawals()
for w in withdrawals:
    print(f"{w['股票名称']} {w['委托类型']} {w['委托数量']}股 @{w['委托价格']}")

# 撤单
result = trader.withdraw("海康威视", "买入", 1000, 10.0)
if result['success']:
    print("撤单成功")

# 添加自选股
result = trader.add_favorite("海康威视")
if result['success']:
    print(f"添加成功，股票代码: {result.get('stock_code', '未获取')}")

# 移除自选股
result = trader.remove_favorite("海康威视")
if result['success']:
    print("移除成功")

# 获取自选股代码
result = trader.get_favorite_code("海康威视")
if result['success']:
    print(f"股票代码: {result['stock_code']}")

# 从自选区买入（无需代码）
result = trader.buy_from_favorite("海康威视", 1000, 31.5)
if result['success']:
    print(f"买入成功: {result['msg']}")

# 从自选区卖出（无需代码）
result = trader.sell_from_favorite("海康威视", 500, 32.0)
if result['success']:
    print(f"卖出成功: {result['msg']}")
```

## 项目结构

```
THSTrader-skill/
├── README.md              # 项目文档
├── requirements.txt       # Python 依赖
├── trader.py             # CLI 入口
└── ths/                  # 核心模块
    ├── __init__.py       # 模块初始化
    ├── config.py         # UI 元素配置
    └── trader.py         # Trader 核心类
```

## 技术实现

### UI 元素定位方式

1. **Resource ID 定位**
   ```python
   self.d(resourceId="com.hexin.plat.android:id/menu_buy_image").click()
   ```

2. **XPath 定位**
   ```python
   self.d.xpath('//*[@content-desc="交易"]/android.widget.ImageView[1]').click()
   ```

3. **坐标定位**（兜底方案）
   ```python
   self.d.click(420, 1210)  # 点击交易标签
   ```

### OCR 文字识别

使用 EasyOCR 识别持仓和撤单列表：

```python
# 截图持仓项
self.d.xpath('...').screenshot().save("tmp.png")

# 裁剪股票名称区域
Image.open("tmp.png").crop((11, 11, 165, 55)).save("tmp.png")

# OCR 识别
result = self.reader.readtext("tmp.png")
stock_name = result[0][1]
```

### 核心流程

#### 买入流程
1. 导航到模拟炒股页面
2. 点击"买入"按钮
3. 输入股票代码（通过 ADB shell）
4. 选择搜索结果
5. 输入价格
6. 输入数量
7. 点击"买入"按钮
8. 二次确认（验证股票代码、数量、价格）
9. 点击"确认买入"
10. OCR 识别结果消息
11. 保存截图

## 与原版 THSTrader 的区别

| 特性 | 原版 THSTrader | THSTrader-skill |
|------|---------------|-----------------|
| 支持版本 | 旧版同花顺 | 新版 11.46.04 |
| 余额查询 | `totalasset_value` | `capital_cell_value` |
| 导航方式 | XPath | XPath + 坐标兜底 |
| CLI 支持 | ❌ | ✅ |
| JSON 输出 | ❌ | ✅ |
| 截图记录 | 部分 | 全流程 |

## 注意事项

1. **分辨率要求**
   - 必须使用 720x1280（竖屏），否则坐标定位会失败
   - 建议 DPI 设置为 240 或 320

2. **模拟炒股**
   - 默认用于模拟炒股，扩展到实盘需要修改代码

3. **OCR 性能**
   - 首次初始化 EasyOCR 较慢（下载模型）
   - 持仓和撤单列表查询速度受 OCR 影响

4. **交易规则**
   - A股 T+1 规则：当天买入的股票，第二天才能卖出
   - 买入数量必须是 100 的整数倍

5. **错误处理**
   - 如遇到"未响应"对话框，脚本会自动点击"等待"
   - 所有交易都有截图记录，失败时查看截图排查

## 常见问题

### Q1: 连接失败

```bash
# 重启 ADB 服务
adb kill-server
adb start-server
adb connect 127.0.0.1:5565
```

### Q2: UI 元素找不到

检查：
1. 同花顺版本是否为 11.46.04
2. 分辨率是否为 720x1280
3. 是否在模拟炒股页面

### Q3: OCR 识别失败

```bash
# 重新安装 easyocr
pip uninstall easyocr
pip install easyocr
```

### Q4: 买入/卖出失败

查看截图文件：
- `buy_<股票代码>_before.png` - 买入前截图
- `buy_<股票代码>_confirm.png` - 确认对话框
- `buy_<股票代码>_after.png` - 买入后截图

## 示例脚本

### 批量买入

```python
from ths import THSTrader

trader = THSTrader()

# 批量买入
stocks = [
    ("002415", 1000, 10.0),   # 海康威视
    ("300033", 1000, 349.0),  # 同花顺
]

for code, amount, price in stocks:
    result = trader.buy(code, amount, price)
    print(f"{code}: {result['msg']}")
```

### 自动止盈止损

```python
from ths import THSTrader

trader = THSTrader()

# 获取持仓
positions = trader.get_position()

for pos in positions:
    # 这里可以根据持仓情况自动卖出
    pass
```

## 开发计划

- [ ] 支持实盘交易
- [ ] 支持更多同花顺版本
- [ ] 添加策略回测功能
- [ ] 优化 OCR 识别速度
- [ ] Web UI 界面

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 致谢

- 原版 [THSTrader](https://github.com/nladuo/THSTrader) 作者
- [uiautomator2](https://github.com/openatx/uiautomator2) 项目
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) 项目

## 免责声明

本项目仅供学习交流使用，不构成任何投资建议。使用本项目进行实盘交易的风险由使用者自行承担。
