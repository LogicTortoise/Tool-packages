#!/usr/bin/env python3
"""
THSTrader 使用示例
"""

from ths import THSTrader


def main():
    # 初始化（连接到设备）
    print("初始化 THSTrader...")
    trader = THSTrader("127.0.0.1:5565")

    # 示例1: 获取账户余额
    print("\n" + "="*60)
    print("示例1: 获取账户余额")
    print("="*60)
    balance = trader.get_balance()
    for key, value in balance.items():
        print(f"  {key}: {value}")

    # 示例2: 获取持仓列表
    print("\n" + "="*60)
    print("示例2: 获取持仓列表")
    print("="*60)
    positions = trader.get_position()
    if positions:
        for i, pos in enumerate(positions, 1):
            print(f"\n  {i}. {pos['股票名称']}")
            print(f"     股票余额: {pos['股票余额']} 股")
            print(f"     可用余额: {pos['可用余额']} 股")
    else:
        print("  暂无持仓")

    # 示例3: 买入股票
    print("\n" + "="*60)
    print("示例3: 买入股票")
    print("="*60)
    result = trader.buy("002415", 100, 10.0)
    print(f"  股票名称: {result['stock_name']}")
    print(f"  状态: {'成功' if result['success'] else '失败'}")
    print(f"  消息: {result['msg']}")

    # 示例4: 获取可撤单列表
    print("\n" + "="*60)
    print("示例4: 获取可撤单列表")
    print("="*60)
    withdrawals = trader.get_avail_withdrawals()
    if withdrawals:
        for i, w in enumerate(withdrawals, 1):
            print(f"\n  {i}. {w['股票名称']} - {w['委托类型']}")
            print(f"     委托价格: {w['委托价格']}")
            print(f"     委托数量: {w['委托数量']} 股")
    else:
        print("  暂无可撤单")

    print("\n" + "="*60)
    print("示例完成")
    print("="*60)


if __name__ == '__main__':
    main()
