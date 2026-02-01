#!/usr/bin/env python3
"""
测试自选股功能
"""

from ths import THSTrader


def test_favorite_operations():
    """测试自选股操作"""
    print("="*60)
    print("测试自选股功能")
    print("="*60)

    trader = THSTrader("127.0.0.1:5565")

    # 测试股票名称
    stock_name = "海康威视"

    # 1. 添加自选股
    print(f"\n1. 添加自选股: {stock_name}")
    result = trader.add_favorite(stock_name)
    print(f"   结果: {result}")

    input("\n按回车继续测试获取代码...")

    # 2. 获取股票代码
    print(f"\n2. 从自选区获取股票代码: {stock_name}")
    result = trader.get_favorite_code(stock_name)
    print(f"   结果: {result}")

    if result['success']:
        stock_code = result['stock_code']
        print(f"   股票代码: {stock_code}")

    input("\n按回车继续测试移除自选...")

    # 3. 移除自选股
    print(f"\n3. 移除自选股: {stock_name}")
    result = trader.remove_favorite(stock_name)
    print(f"   结果: {result}")

    print("\n"+"="*60)
    print("自选股功能测试完成")
    print("="*60)


def test_trade_from_favorite():
    """测试从自选区交易"""
    print("="*60)
    print("测试从自选区交易功能")
    print("="*60)

    trader = THSTrader("127.0.0.1:5565")

    stock_name = "海康威视"
    amount = 100
    price = 31.5

    # 确保股票在自选中
    print(f"\n确保 {stock_name} 在自选中...")
    trader.add_favorite(stock_name)

    input("\n按回车继续测试从自选区买入...")

    # 测试从自选区买入
    print(f"\n测试从自选区买入: {stock_name} {amount}股 @{price}")
    result = trader.buy_from_favorite(stock_name, amount, price)
    print(f"结果: {result}")

    print("\n"+"="*60)
    print("从自选区交易测试完成")
    print("="*60)


if __name__ == '__main__':
    import sys

    print("""
自选股功能测试脚本

请确保:
1. BlueStacks 模拟器正在运行 (127.0.0.1:5565)
2. 同花顺 APP 已登录
3. 模拟炒股功能可用

测试选项:
1. 测试自选股基本操作（添加、获取代码、移除）
2. 测试从自选区交易
0. 退出

注意: 测试 2 会执行实际买入操作（模拟炒股）
    """)

    choice = input("请选择测试项 (1/2/0): ").strip()

    if choice == '1':
        test_favorite_operations()
    elif choice == '2':
        test_trade_from_favorite()
    elif choice == '0':
        print("退出测试")
        sys.exit(0)
    else:
        print("无效选择")
        sys.exit(1)
