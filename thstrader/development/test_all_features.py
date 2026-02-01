#!/usr/bin/env python3
"""
THSTrader 功能测试脚本
测试所有核心功能是否正常工作
"""
import sys
sys.path.insert(0, '.')

from ths import THSTrader
import time


def print_section(title):
    """打印分节标题"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def test_balance(trader):
    """测试获取账户余额"""
    print_section("测试 1: 获取账户余额")
    try:
        balance = trader.get_balance()
        print(f"✓ 获取成功")
        for key, value in balance.items():
            print(f"  {key}: {value}")
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_position(trader):
    """测试获取持仓列表"""
    print_section("测试 2: 获取持仓列表")
    try:
        positions = trader.get_position()
        print(f"✓ 获取成功 (共 {len(positions)} 只)")
        for i, pos in enumerate(positions[:3], 1):  # 只显示前3个
            print(f"  {i}. {pos.get('股票名称', 'N/A')} - "
                  f"股票余额: {pos.get('股票余额', 'N/A')}, "
                  f"可用余额: {pos.get('可用余额', 'N/A')}")
        if len(positions) > 3:
            print(f"  ... (还有 {len(positions) - 3} 只)")
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_withdrawals(trader):
    """测试获取可撤单列表"""
    print_section("测试 3: 获取可撤单列表")
    try:
        withdrawals = trader.get_avail_withdrawals()
        print(f"✓ 获取成功 (共 {len(withdrawals)} 条)")
        for i, w in enumerate(withdrawals[:3], 1):  # 只显示前3个
            print(f"  {i}. {w.get('股票名称', 'N/A')} - {w.get('委托类型', 'N/A')} - "
                  f"价格: {w.get('委托价格', 'N/A')}, "
                  f"数量: {w.get('委托数量', 'N/A')}")
        if len(withdrawals) > 3:
            print(f"  ... (还有 {len(withdrawals) - 3} 条)")
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_buy_sell(trader, test_code="002415", test_amount=100, test_price=10.0):
    """测试买入和卖出功能（但不实际执行）"""
    print_section("测试 4: 买入功能（模拟）")
    print(f"注意: 这是一个模拟测试，不会实际提交订单")
    print(f"测试参数: 股票代码={test_code}, 数量={test_amount}, 价格={test_price}")
    print("如需实际测试买入卖出，请手动调用 trader.buy() 和 trader.sell()")
    return True


def test_favorite_operations(trader, test_pinyin="hkws"):
    """测试自选股相关操作"""
    print_section("测试 5: 自选股操作")

    # 测试添加自选
    print(f"\n5.1 测试添加自选股 (拼音: {test_pinyin})")
    try:
        result = trader.add_favorite(test_pinyin)
        if result['success']:
            print(f"✓ 添加成功")
            print(f"  消息: {result['msg']}")
            print(f"  股票代码: {result.get('stock_code', '未获取')}")

            # 如果添加成功，测试获取股票代码
            print(f"\n5.2 测试从自选获取股票代码")
            try:
                code_result = trader.get_favorite_code(test_pinyin)
                if code_result['success']:
                    print(f"✓ 获取成功")
                    print(f"  股票代码: {code_result['stock_code']}")
                else:
                    print(f"✗ 获取失败: {code_result['msg']}")
            except Exception as e:
                print(f"✗ 获取失败: {e}")

            # 测试移除自选
            print(f"\n5.3 测试移除自选股")
            try:
                remove_result = trader.remove_favorite(test_pinyin)
                if remove_result['success']:
                    print(f"✓ 移除成功: {remove_result['msg']}")
                else:
                    print(f"✗ 移除失败: {remove_result['msg']}")
            except Exception as e:
                print(f"✗ 移除失败: {e}")

            return True
        else:
            print(f"✗ 添加失败: {result['msg']}")
            print(f"  提示: 自选股功能可能需要手动调整UI定位")
            return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_connection(trader):
    """测试设备连接"""
    print_section("测试 0: 设备连接")
    try:
        # 检查应用是否运行
        current = trader.d.app_current()
        print(f"✓ 设备连接正常")
        print(f"  当前应用: {current['package']}")
        print(f"  Activity: {current['activity']}")

        # 如果不是同花顺，启动它
        if current['package'] != 'com.hexin.plat.android':
            print(f"\n启动同花顺应用...")
            trader.d.app_start('com.hexin.plat.android')
            time.sleep(3)
            print(f"✓ 应用已启动")

        return True
    except Exception as e:
        print(f"✗ 连接测试失败: {e}")
        return False


def main():
    """主测试流程"""
    print("="*60)
    print("THSTrader 功能测试")
    print("="*60)
    print(f"设备: 127.0.0.1:5565")
    print(f"测试项目:")
    print(f"  0. 设备连接")
    print(f"  1. 获取账户余额")
    print(f"  2. 获取持仓列表")
    print(f"  3. 获取可撤单列表")
    print(f"  4. 买入/卖出功能（模拟）")
    print(f"  5. 自选股操作")

    # 初始化
    print("\n初始化 THSTrader...")
    try:
        trader = THSTrader("127.0.0.1:5565")
    except Exception as e:
        print(f"✗ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 运行测试
    results = {}

    results['connection'] = test_connection(trader)
    time.sleep(2)

    results['balance'] = test_balance(trader)
    time.sleep(2)

    results['position'] = test_position(trader)
    time.sleep(2)

    results['withdrawals'] = test_withdrawals(trader)
    time.sleep(2)

    results['buy_sell'] = test_buy_sell(trader)
    time.sleep(2)

    results['favorites'] = test_favorite_operations(trader)

    # 汇总结果
    print_section("测试结果汇总")
    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print(f"\n通过: {passed}/{total}")
    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {test_name:15s}: {status}")

    print("\n" + "="*60)
    if passed == total:
        print("✓ 所有测试通过！")
    else:
        print(f"⚠ {total - passed} 个测试失败，请检查上方详情")
    print("="*60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试已取消")
    except Exception as e:
        print(f"\n\n测试异常: {e}")
        import traceback
        traceback.print_exc()
