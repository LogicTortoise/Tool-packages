---
name: thstrader
description: "Automate stock trading operations on TongHuaShun (同花顺) mobile app for simulated trading. Use when working with stock trading tasks including: (1) Query account balance and positions, (2) Buy or sell stocks, (3) Manage pending orders and cancellations, (4) Automate trading strategies. Works with Android emulator (BlueStacks) via ADB and uiautomator2."
---

# THS Trader - 同花顺自动交易

Automate stock trading operations on TongHuaShun (同花顺) mobile app through Android emulator.

## Quick Start

### Prerequisites

1. **BlueStacks emulator** running at 127.0.0.1:5565
2. **Resolution**: 720x1280 (portrait) - CRITICAL
3. **TongHuaShun app** (version 11.46.04) installed and logged in
4. **Simulated trading account** active and accessible

See [setup.md](references/setup.md) for detailed installation guide.

### Install Dependencies

```bash
cd scripts/
pip install -r requirements.txt
```

### Verify Setup

```bash
python trader.py balance --device 127.0.0.1:5565
```

## Core Operations

### 1. Query Account Balance

**CLI**:
```bash
python trader.py balance [--device DEVICE] [--json]
```

**Python API**:
```python
from ths import THSTrader

trader = THSTrader("127.0.0.1:5565")
balance = trader.get_balance()

print(f"Total Assets: {balance['总资产']}")
print(f"Available: {balance['可用']}")
print(f"P/L: {balance['浮动盈亏']}")
```

Returns account summary including total assets, available funds, frozen funds, position value, and P/L.

### 2. View Positions

**CLI**:
```bash
python trader.py position [--device DEVICE] [--json]
```

**Python API**:
```python
positions = trader.get_position()

for pos in positions:
    print(f"{pos['股票名称']} ({pos['股票代码']}): {pos['股票余额']}股")
    print(f"  Cost: ¥{pos['成本价']}, Current: ¥{pos['现价']}")
    print(f"  P/L: {pos['浮动盈亏']} ({pos['盈亏比例']})")
```

Returns list of all holdings with stock name, code, quantity, cost, current price, and P/L.

### 3. Buy Stock

**CLI**:
```bash
python trader.py buy --code 002415 --amount 1000 --price 10.0 [--device DEVICE]
```

**Python API**:
```python
# Buy 1000 shares of 海康威视 (002415) at ¥10.0
result = trader.buy("002415", 1000, 10.0)

if result['success']:
    print(f"Buy order submitted: {result['msg']}")
else:
    print(f"Buy failed: {result['msg']}")
```

**Parameters**:
- `code`: 6-digit stock code (e.g., "002415")
- `amount`: Number of shares (must be multiple of 100)
- `price`: Limit price

**Process**:
1. Navigate to simulated trading page
2. Click buy button
3. Input stock code
4. Select from search results
5. Input price and amount
6. Confirm purchase
7. Auto-verify order details
8. Submit order
9. Save screenshots for verification

Screenshots saved: `buy_<code>_before.png`, `buy_<code>_confirm.png`, `buy_<code>_after.png`

### 4. Sell Stock

**CLI**:
```bash
python trader.py sell --code 002415 --amount 500 --price 11.0 [--device DEVICE]
```

**Python API**:
```python
# Sell 500 shares at ¥11.0
result = trader.sell("002415", 500, 11.0)

if result['success']:
    print(f"Sell order submitted: {result['msg']}")
```

**Important**: A-share T+1 rule - stocks bought today can only be sold tomorrow.

### 5. Manage Pending Orders

**View pending orders**:
```bash
python trader.py withdrawals [--device DEVICE] [--json]
```

```python
withdrawals = trader.get_avail_withdrawals()

for w in withdrawals:
    print(f"{w['股票名称']} {w['委托类型']} {w['委托数量']}股 @¥{w['委托价格']}")
    print(f"  Status: {w['状态']}")
```

**Cancel order**:
```bash
python trader.py cancel --name 海康威视 --type 买入 --amount 1000 --price 10.0
```

```python
# Cancel specific order (must match exactly)
result = trader.withdraw("海康威视", "买入", 1000, 10.0)

if result['success']:
    print("Order cancelled successfully")
```

**Important**: Parameters (name, type, amount, price) must EXACTLY match the pending order.

## Common Patterns

### Batch Buy Multiple Stocks

```python
from ths import THSTrader

trader = THSTrader()

stocks = [
    ("002415", 1000, 10.0),   # 海康威视
    ("300033", 1000, 349.0),  # 同花顺
]

for code, amount, price in stocks:
    result = trader.buy(code, amount, price)
    print(f"{code}: {result['msg']}")
```

### Auto Stop-Loss/Take-Profit

```python
positions = trader.get_position()

for pos in positions:
    cost = float(pos['成本价'].replace(',', ''))
    current = float(pos['现价'].replace(',', ''))
    code = pos['股票代码']
    amount = int(pos['可用余额'].replace(',', ''))

    # Take profit: >10% gain
    if current >= cost * 1.1:
        trader.sell(code, amount, current)

    # Stop loss: >5% loss
    elif current <= cost * 0.95:
        trader.sell(code, amount, current)
```

### Cancel All Pending Orders

```python
withdrawals = trader.get_avail_withdrawals()

for w in withdrawals:
    trader.withdraw(
        w['股票名称'],
        w['委托类型'],
        int(w['委托数量'].replace(',', '')),
        float(w['委托价格'].replace(',', ''))
    )
```

## References

For detailed information, see:

- **[setup.md](references/setup.md)** - Complete installation and configuration guide
  - Hardware/software requirements
  - BlueStacks setup
  - ADB connection
  - App installation

- **[api-reference.md](references/api-reference.md)** - Complete API documentation
  - All method signatures and return values
  - CLI command reference
  - Trading rules (A-share T+1, lot size, etc.)
  - Complete code examples

- **[troubleshooting.md](references/troubleshooting.md)** - Common issues and solutions
  - ADB connection issues
  - UI element not found
  - OCR recognition failures
  - Trading operation failures

## Important Notes

### Critical Requirements

⚠️ **Resolution MUST be 720x1280** (portrait) - coordinate-based clicks will fail otherwise
⚠️ **TongHuaShun version MUST be 11.46.04** - UI elements differ in other versions
⚠️ **DPI should be 240 or 320**
⚠️ **Only supports simulated trading** - extending to real trading requires code modifications

### Trading Rules

- **Lot size**: Buy/sell amounts must be multiples of 100 (1 lot = 100 shares)
- **T+1 rule**: Stocks bought today can only be sold tomorrow
- **Order matching**: Cancel order parameters must EXACTLY match pending order details

### Screenshots

All trading operations auto-save screenshots to current directory for verification and debugging:
- Before/confirm/after screenshots for each buy/sell operation
- Check these if operations fail or produce unexpected results

### UI Automation

- Uses **Resource ID** + **XPath** + **coordinate clicking**
- Automatically handles "App not responding" dialogs
- OCR (EasyOCR) for reading position and pending order details
- First-time OCR model download may take several minutes

### Device Connection

Default device: `127.0.0.1:5565` (BlueStacks)

For other emulators, specify device:
```bash
python trader.py balance --device <device_id>
```

Get device list:
```bash
adb devices
```
