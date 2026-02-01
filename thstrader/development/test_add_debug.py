#!/usr/bin/env python3
"""
测试添加自选 - 调试版本，每步截图
"""
import sys
sys.path.insert(0, '.')

from ths import THSTrader
import time

print("="*60)
print("调试测试：添加海康威视到自选")
print("="*60)

# 初始化 trader
trader = THSTrader("127.0.0.1:5565")

# 检查当前应用
current_app = trader.d.app_current()
print(f"\n当前应用: {current_app}")

# 如果不是同花顺，启动同花顺
if current_app['package'] != 'com.hexin.plat.android':
    print("\n启动同花顺应用...")
    trader.d.app_start('com.hexin.plat.android')
    time.sleep(5)

# 截图1: 初始状态
trader.d.screenshot("screenshot_1_initial.png")
print("\n✓ 截图1: 初始状态 -> screenshot_1_initial.png")

# 点击自选tab
print("\n点击自选tab...")
if trader.d(text="自选").exists:
    print("  找到'自选'文字，点击...")
    trader.d(text="自选").click()
else:
    print("  未找到'自选'文字，使用坐标 (140, 1210)")
    trader.d.click(140, 1210)
time.sleep(2)

# 截图2: 自选tab
trader.d.screenshot("screenshot_2_favorites_tab.png")
print("✓ 截图2: 自选tab -> screenshot_2_favorites_tab.png")

# 点击搜索按钮
print("\n点击右上角搜索按钮...")
# 尝试多个位置
positions = [(680, 80), (650, 100), (600, 80)]
for i, (x, y) in enumerate(positions):
    print(f"  尝试位置 {i+1}: ({x}, {y})")
    trader.d.click(x, y)
    time.sleep(2)

    # 截图
    trader.d.screenshot(f"screenshot_3_{i+1}_after_search_click.png")
    print(f"✓ 截图3-{i+1}: 点击搜索后 -> screenshot_3_{i+1}_after_search_click.png")

    # 检查是否有输入框出现
    if trader.d(resourceId="com.hexin.plat.android:id/content_stock").exists:
        print(f"  ✓ 找到输入框！位置正确: ({x}, {y})")
        break
    else:
        print(f"  ✗ 未找到输入框，尝试下一个位置...")
        trader.d.press("back")
        time.sleep(1)

# 输入搜索关键词
print("\n输入搜索关键词: hkws")
trader.d.send_keys("hkws")
time.sleep(2)

# 截图4: 输入后
trader.d.screenshot("screenshot_4_after_input.png")
print("✓ 截图4: 输入后 -> screenshot_4_after_input.png")

# 检查搜索结果
print("\n检查搜索结果...")
if trader.d(resourceId="com.hexin.plat.android:id/stockname_tv").exists:
    print("  ✓ 找到搜索结果！")
    try:
        stock_name = trader.d(resourceId="com.hexin.plat.android:id/stockname_tv").get_text()
        print(f"  第一个结果: {stock_name}")
    except:
        print("  无法获取股票名称")
else:
    print("  ✗ 未找到搜索结果")

# 截图5: 最终状态
trader.d.screenshot("screenshot_5_final.png")
print("✓ 截图5: 最终状态 -> screenshot_5_final.png")

print("\n" + "="*60)
print("测试完成！请查看截图文件了解每步的UI状态")
print("="*60)
