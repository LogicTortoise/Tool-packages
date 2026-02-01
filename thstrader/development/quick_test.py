#!/usr/bin/env python3
"""
快速测试脚本 - 验证 THSTrader 核心功能
"""

import sys

def test_imports():
    """测试模块导入"""
    print("测试 1/3: 模块导入...")
    try:
        from ths import THSTrader
        from ths.config import UI_ELEMENTS, COORDINATES
        print("  ✓ 模块导入成功")
        return True
    except Exception as e:
        print(f"  ✗ 模块导入失败: {e}")
        return False


def test_connection():
    """测试设备连接"""
    print("\n测试 2/3: 设备连接...")
    try:
        from ths import THSTrader
        trader = THSTrader("127.0.0.1:5565")
        print("  ✓ 设备连接成功")
        return True
    except Exception as e:
        print(f"  ✗ 设备连接失败: {e}")
        return False


def test_config():
    """测试配置文件"""
    print("\n测试 3/3: 配置验证...")
    try:
        from ths.config import UI_ELEMENTS, COORDINATES, XPATHS

        # 检查关键配置
        assert "menu_buy_image" in UI_ELEMENTS
        assert "trading_tab" in COORDINATES
        assert "trading_tab" in XPATHS

        print(f"  ✓ 配置验证成功")
        print(f"    - UI元素: {len(UI_ELEMENTS)} 个")
        print(f"    - 坐标点: {len(COORDINATES)} 个")
        print(f"    - XPath: {len(XPATHS)} 个")
        return True
    except Exception as e:
        print(f"  ✗ 配置验证失败: {e}")
        return False


def main():
    print("="*60)
    print("THSTrader 快速测试")
    print("="*60)

    results = []
    results.append(test_imports())
    results.append(test_connection())
    results.append(test_config())

    print("\n" + "="*60)
    print("测试结果")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("\n✓ 所有测试通过！")
        return 0
    else:
        print("\n✗ 部分测试失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())
