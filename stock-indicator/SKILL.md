---
name: stock-indicator
description: "Query A-share stock technical indicators (KDJ, MACD) using AkShare and Pandas-TA. Use when the user asks about stock indicators, technical analysis, KDJ, MACD, or wants to check stock signals for A-share symbols. Example: 'stock_indicator 000001 5'."
---

# Stock Indicator

Query KDJ and MACD technical indicators for A-share stocks.

## Prerequisites

- Python virtual environment at `~/agent-venv` with `akshare`, `pandas_ta`, `pandas` installed

## Usage

```bash
~/agent-venv/bin/python {baseDir}/indicator.py <symbol> [--days N]
```

### Examples

```bash
# Query last 5 days of indicators for 平安银行 (000001)
~/agent-venv/bin/python {baseDir}/indicator.py 000001 --days 5

# Query last 10 days for 贵州茅台 (600519)
~/agent-venv/bin/python {baseDir}/indicator.py 600519 --days 10
```

## Output

JSON array with daily records containing: Date, Open, Close, High, Low, Volume, K_9_3, D_9_3, J_9_3, MACD, MACDh, MACDs.
