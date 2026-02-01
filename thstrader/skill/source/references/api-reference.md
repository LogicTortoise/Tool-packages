# API 参考文档

## Python API

### 初始化

```python
from ths import THSTrader

# 使用默认设备
trader = THSTrader()

# 指定设备
trader = THSTrader("127.0.0.1:5565")
```

### 获取账户余额

```python
balance = trader.get_balance()
```

**返回值** (dict):
```python
{
    '总资产': '200,000.00',
    '可用': '180,000.00',
    '冻结': '0.00',
    '持仓市值': '20,000.00',
    '浮动盈亏': '+1,234.56',
    '盈亏比例': '+6.17%'
}
```

### 获取持仓列表

```python
positions = trader.get_position()
```

**返回值** (list[dict]):
```python
[
    {
        '股票名称': '海康威视',
        '股票代码': '002415',
        '股票余额': '1000',
        '可用余额': '1000',
        '成本价': '30.00',
        '现价': '31.00',
        '浮动盈亏': '+1,000.00',
        '盈亏比例': '+3.33%'
    },
    # ... 更多持仓
]
```

### 买入股票

```python
result = trader.buy(stock_code, amount, price)
```

**参数**:
- `stock_code` (str): 股票代码 (6位数字，如 "002415")
- `amount` (int): 买入数量 (必须是100的整数倍)
- `price` (float): 买入价格

**返回值** (dict):
```python
{
    'success': True,
    'msg': '委托已提交'
}
```

**示例**:
```python
# 买入1000股海康威视，价格10.0元
result = trader.buy("002415", 1000, 10.0)
if result['success']:
    print(f"买入成功: {result['msg']}")
else:
    print(f"买入失败: {result['msg']}")
```

### 卖出股票

```python
result = trader.sell(stock_code, amount, price)
```

**参数**:
- `stock_code` (str): 股票代码
- `amount` (int): 卖出数量
- `price` (float): 卖出价格

**返回值** (dict):
```python
{
    'success': True,
    'msg': '委托已提交'
}
```

**示例**:
```python
# 卖出500股海康威视，价格11.0元
result = trader.sell("002415", 500, 11.0)
if result['success']:
    print(f"卖出成功: {result['msg']}")
```

**注意**: A股 T+1 规则 - 当天买入的股票，第二天才能卖出

### 获取可撤单列表

```python
withdrawals = trader.get_avail_withdrawals()
```

**返回值** (list[dict]):
```python
[
    {
        '股票名称': '海康威视',
        '股票代码': '002415',
        '委托类型': '买入',
        '委托数量': '1000',
        '委托价格': '10.0',
        '成交数量': '0',
        '状态': '未成交'
    },
    # ... 更多委托
]
```

### 撤单

```python
result = trader.withdraw(stock_name, trade_type, amount, price)
```

**参数**:
- `stock_name` (str): 股票名称 (如 "海康威视")
- `trade_type` (str): 委托类型 ("买入" 或 "卖出")
- `amount` (int): 委托数量
- `price` (float): 委托价格

**返回值** (dict):
```python
{
    'success': True,
    'msg': '撤单成功'
}
```

**示例**:
```python
# 撤销买入海康威视1000股@10.0的委托
result = trader.withdraw("海康威视", "买入", 1000, 10.0)
if result['success']:
    print("撤单成功")
```

**注意**: 参数必须与可撤单列表中的信息完全一致

## 命令行接口 (CLI)

### 查看帮助

```bash
python trader.py --help
```

### 获取账户余额

```bash
python trader.py balance [--device DEVICE] [--json]
```

**示例**:
```bash
# 默认设备
python trader.py balance

# 指定设备
python trader.py balance --device 127.0.0.1:5565

# JSON 格式输出
python trader.py balance --json
```

### 获取持仓列表

```bash
python trader.py position [--device DEVICE] [--json]
```

### 买入股票

```bash
python trader.py buy --code CODE --amount AMOUNT --price PRICE [--device DEVICE]
```

**示例**:
```bash
python trader.py buy --code 002415 --amount 1000 --price 10.0
```

### 卖出股票

```bash
python trader.py sell --code CODE --amount AMOUNT --price PRICE [--device DEVICE]
```

**示例**:
```bash
python trader.py sell --code 002415 --amount 500 --price 11.0
```

### 查看可撤单列表

```bash
python trader.py withdrawals [--device DEVICE] [--json]
```

### 撤单

```bash
python trader.py cancel --name NAME --type TYPE --amount AMOUNT --price PRICE [--device DEVICE]
```

**示例**:
```bash
python trader.py cancel --name 海康威视 --type 买入 --amount 1000 --price 10.0
```

## 完整示例

### 批量买入

```python
from ths import THSTrader

trader = THSTrader()

# 批量买入多只股票
stocks = [
    ("002415", 1000, 10.0),   # 海康威视
    ("300033", 1000, 349.0),  # 同花顺
    ("600519", 100, 1800.0),  # 贵州茅台
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
    code = pos['股票代码']
    name = pos['股票名称']
    cost = float(pos['成本价'].replace(',', ''))
    current = float(pos['现价'].replace(',', ''))
    amount = int(pos['可用余额'].replace(',', ''))

    # 止盈: 涨幅超过10%
    if current >= cost * 1.1:
        result = trader.sell(code, amount, current)
        print(f"止盈卖出 {name}: {result['msg']}")

    # 止损: 跌幅超过5%
    elif current <= cost * 0.95:
        result = trader.sell(code, amount, current)
        print(f"止损卖出 {name}: {result['msg']}")
```

### 撤销所有未成交委托

```python
from ths import THSTrader

trader = THSTrader()

# 获取所有可撤单
withdrawals = trader.get_avail_withdrawals()

for w in withdrawals:
    name = w['股票名称']
    trade_type = w['委托类型']
    amount = int(w['委托数量'].replace(',', ''))
    price = float(w['委托价格'].replace(',', ''))

    result = trader.withdraw(name, trade_type, amount, price)
    print(f"撤单 {name} {trade_type} {amount}股 @{price}: {result['msg']}")
```

## 交易规则

### A股交易规则

1. **T+1 规则**: 当天买入的股票，第二天才能卖出
2. **买入数量**: 必须是 100 的整数倍 (1手 = 100股)
3. **涨跌停限制**:
   - 主板: ±10%
   - 创业板/科创板: ±20%
   - ST 股票: ±5%
4. **交易时间**:
   - 9:30 - 11:30 (上午)
   - 13:00 - 15:00 (下午)

### 模拟炒股特殊规则

1. **初始资金**: 通常为 100,000 或 200,000 元
2. **无需真实资金**: 所有交易都是模拟的
3. **实时行情**: 使用真实市场行情
4. **无手续费**: 部分模拟炒股平台不收取手续费

## 错误处理

所有方法在发生错误时会返回带有错误信息的字典:

```python
{
    'success': False,
    'msg': '错误描述'
}
```

建议始终检查 `success` 字段:

```python
result = trader.buy("002415", 1000, 10.0)
if not result['success']:
    print(f"操作失败: {result['msg']}")
    # 进行错误处理...
```

## 截图记录

所有交易操作都会自动保存截图到当前目录:

- `buy_<股票代码>_before.png` - 买入前
- `buy_<股票代码>_confirm.png` - 确认对话框
- `buy_<股票代码>_after.png` - 买入后
- `sell_<股票代码>_before.png` - 卖出前
- `sell_<股票代码>_confirm.png` - 确认对话框
- `sell_<股票代码>_after.png` - 卖出后

这些截图可用于:
1. 验证操作是否成功
2. 排查问题
3. 记录交易历史
