#!/usr/bin/env python3
"""
测试添加消费ETF到自选
"""
import sys
sys.path.insert(0, '.')

from ths import THSTrader

print("="*60)
print("测试添加消费ETF到自选")
print("="*60)

# 初始化 trader
trader = THSTrader("127.0.0.1:5565")

# 添加消费ETF（拼音首字母: xfetf）
print("\n添加消费ETF（拼音: xfetf）...")
result = trader.add_favorite("xfetf")

print("\n结果:")
print(f"  成功: {result['success']}")
print(f"  消息: {result['msg']}")
print(f"  股票代码: {result.get('stock_code', '未获取')}")

print("\n="*60)
if result['success']:
    print("✓ 添加成功！")
else:
    print("✗ 添加失败")
print("="*60)
