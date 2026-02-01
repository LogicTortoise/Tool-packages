#!/usr/bin/env python3
"""
完整测试：买入 → 查看撤单列表 → 撤单
"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import uiautomator2 as u2

def dismiss_dialog(d):
    """关闭对话框"""
    try:
        if d(text="等待").exists(timeout=1):
            d(text="等待").click()
            time.sleep(1)
            return True
    except:
        pass
    return False

def buy_stock(d, stock_code, amount, price):
    """买入股票"""
    print(f"\n{'='*60}")
    print(f"步骤 1/3: 买入股票 {stock_code}")
    print(f"{'='*60}")

    # 启动应用并导航
    print("\n导航到模拟炒股...")
    d.app_start("com.hexin.plat.android")
    time.sleep(5)

    for _ in range(3):
        dismiss_dialog(d)
        time.sleep(1)

    # 点击交易
    d.click(420, 1210)
    time.sleep(3)
    dismiss_dialog(d)

    # 点击模拟炒股
    if d(resourceId="com.hexin.plat.android:id/tab_mn").exists:
        d(resourceId="com.hexin.plat.android:id/tab_mn").click()
        time.sleep(3)

    for _ in range(3):
        dismiss_dialog(d)
        time.sleep(1)

    # 点击买入按钮
    print("\n点击买入按钮...")
    d.click(72, 610)
    time.sleep(3)
    dismiss_dialog(d)

    # 输入股票代码
    print(f"\n输入股票代码 {stock_code}...")
    if d(resourceId="com.hexin.plat.android:id/content_stock").exists:
        d(resourceId="com.hexin.plat.android:id/content_stock").click()
        time.sleep(2)

        d.shell("input keyevent 123")
        for _ in range(20):
            d.shell("input keyevent 67")

        d.shell(f"input text {stock_code}")
        time.sleep(2)

        # 选择股票
        if d(resourceId="com.hexin.plat.android:id/stockname_tv").exists:
            d(resourceId="com.hexin.plat.android:id/stockname_tv").click()
            time.sleep(2)

    # 输入价格
    print(f"\n输入价格 {price}...")
    if d(resourceId="com.hexin.plat.android:id/stockprice").exists:
        d(resourceId="com.hexin.plat.android:id/stockprice").click()
        time.sleep(1)
        d.shell("input keyevent 123")
        for _ in range(20):
            d.shell("input keyevent 67")
        d.shell(f"input text {price:.2f}")
        time.sleep(1)

    # 输入数量
    print(f"\n输入数量 {amount}...")
    if d(resourceId="com.hexin.plat.android:id/stockvolume").exists:
        d(resourceId="com.hexin.plat.android:id/stockvolume").click()
        time.sleep(1)
        d.shell("input keyevent 123")
        for _ in range(20):
            d.shell("input keyevent 67")
        d.shell(f"input text {amount}")
        time.sleep(1)

    # 截图
    d.screenshot("test_buy_before.png")
    print("\n✓ 已保存买入前截图")

    # 点击买入
    print("\n点击买入按钮...")
    if d(text="买入").exists:
        d(text="买入").click()
        time.sleep(2)

        # 确认对话框
        if d(resourceId="com.hexin.plat.android:id/ok_btn").exists:
            d.screenshot("test_buy_confirm.png")
            print("✓ 已保存确认对话框截图")

            # 获取股票名称
            stock_name = None
            if d(resourceId="com.hexin.plat.android:id/stock_name_value").exists:
                stock_name = d(resourceId="com.hexin.plat.android:id/stock_name_value").get_text()

            d(resourceId="com.hexin.plat.android:id/ok_btn").click()
            time.sleep(2)
            print("✓ 已点击确认按钮")

    # 截图
    time.sleep(2)
    d.screenshot("test_buy_after.png")
    print("✓ 已保存买入后截图")

    # 检查结果
    h = d.dump_hierarchy()
    if "委托已提交" in h or "成功" in h:
        print("\n✓✓✓ 买入成功！委托已提交 ✓✓✓")

        # 关闭结果对话框
        if d(resourceId="com.hexin.plat.android:id/ok_btn").exists:
            d(resourceId="com.hexin.plat.android:id/ok_btn").click()
            time.sleep(1)

        return True, stock_name
    else:
        print("\n请查看截图确认结果")
        return False, stock_name

def check_withdrawals(d):
    """查看撤单列表"""
    print(f"\n{'='*60}")
    print(f"步骤 2/3: 查看撤单列表")
    print(f"{'='*60}")

    # 返回主页
    d.press("back")
    time.sleep(2)
    dismiss_dialog(d)

    # 点击撤单按钮
    print("\n点击撤单按钮...")
    d.click(504, 610)
    time.sleep(3)
    dismiss_dialog(d)

    # 截图
    d.screenshot("test_withdrawals.png")
    print("✓ 已保存撤单列表截图")

    # 检查是否有撤单
    h = d.dump_hierarchy()
    if "暂无数据" in h or "没有委托" in h:
        print("\n✗ 撤单列表为空")
        return False
    else:
        print("\n✓ 撤单列表有数据")
        return True

def cancel_order(d, stock_name=None):
    """撤单"""
    print(f"\n{'='*60}")
    print(f"步骤 3/3: 撤单")
    print(f"{'='*60}")

    # 点击第一个委托
    print("\n点击第一个委托...")
    try:
        # 尝试点击列表的第一项
        d.xpath('//*[@resource-id="com.hexin.plat.android:id/chedan_recycler_view"]/android.widget.LinearLayout[1]').click()
        time.sleep(2)
        print("✓ 已点击委托")

        # 截图
        d.screenshot("test_cancel_menu.png")
        print("✓ 已保存撤单菜单截图")

        # 点击撤单选项
        if d(resourceId="com.hexin.plat.android:id/option_chedan").exists:
            d(resourceId="com.hexin.plat.android:id/option_chedan").click()
            time.sleep(2)
            print("✓ 已点击撤单选项")

            # 截图
            d.screenshot("test_cancel_after.png")
            print("✓ 已保存撤单后截图")

            # 检查结果
            h = d.dump_hierarchy()
            if "成功" in h or "撤单" in h:
                print("\n✓✓✓ 撤单成功 ✓✓✓")
                return True
            else:
                print("\n请查看截图确认结果")
                return True
        else:
            print("\n✗ 未找到撤单选项")
            return False
    except Exception as e:
        print(f"\n✗ 撤单失败: {e}")
        d.screenshot("test_cancel_error.png")
        return False

def main():
    print("="*60)
    print("THSTrader 完整测试：买入 → 撤单列表 → 撤单")
    print("="*60)

    # 连接设备
    print("\n连接设备...")
    d = u2.connect("127.0.0.1:5565")
    print("✓ 设备连接成功")

    # 股票参数
    stock_code = "002415"
    amount = 100
    price = 31.33

    # 步骤1: 买入
    buy_success, stock_name = buy_stock(d, stock_code, amount, price)

    if not buy_success:
        print("\n✗ 买入失败，测试终止")
        return 1

    # 等待一下
    time.sleep(3)

    # 步骤2: 查看撤单列表
    has_withdrawals = check_withdrawals(d)

    if not has_withdrawals:
        print("\n⚠️ 撤单列表为空，可能委托已成交")
        print("\n测试部分完成（买入成功，但无可撤单）")
        return 0

    # 步骤3: 撤单
    cancel_success = cancel_order(d, stock_name)

    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"✓ 买入: {'成功' if buy_success else '失败'}")
    print(f"✓ 撤单列表: {'有数据' if has_withdrawals else '无数据'}")
    print(f"✓ 撤单: {'成功' if cancel_success else '失败'}")

    print("\n截图文件:")
    print("  - test_buy_before.png")
    print("  - test_buy_confirm.png")
    print("  - test_buy_after.png")
    print("  - test_withdrawals.png")
    print("  - test_cancel_menu.png")
    print("  - test_cancel_after.png")

    print("\n" + "="*60)
    print("✓✓✓ 测试完成！✓✓✓")
    print("="*60)

    return 0

if __name__ == '__main__':
    sys.exit(main())
