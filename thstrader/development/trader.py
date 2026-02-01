#!/usr/bin/env python3
"""
THSTrader CLI 入口
支持多个命令：获取余额、获取持仓、买入、卖出、获取撤单列表、撤单

使用示例:
    python trader.py balance --device 127.0.0.1:5565
    python trader.py position --device 127.0.0.1:5565
    python trader.py buy --code 002415 --amount 1000 --price 10.0
    python trader.py sell --code 002415 --amount 500 --price 11.0
    python trader.py withdrawals
    python trader.py cancel --name 海康威视 --type 买入 --amount 1000 --price 10.0
"""

import argparse
import sys
import json
from ths import THSTrader


def cmd_balance(args):
    """获取账户余额"""
    trader = THSTrader(args.device)
    balance = trader.get_balance()

    print("\n" + "="*60)
    print("账户余额")
    print("="*60)
    for key, value in balance.items():
        print(f"  {key:12s}: {value}")
    print("="*60)

    if args.json:
        print(json.dumps(balance, ensure_ascii=False, indent=2))


def cmd_position(args):
    """获取持仓列表"""
    trader = THSTrader(args.device)
    positions = trader.get_position()

    print("\n" + "="*60)
    print(f"持仓列表 (共 {len(positions)} 只)")
    print("="*60)
    for i, pos in enumerate(positions, 1):
        print(f"\n{i}. {pos['股票名称']}")
        print(f"   股票余额: {pos['股票余额']} 股")
        print(f"   可用余额: {pos['可用余额']} 股")
    print("="*60)

    if args.json:
        print(json.dumps(positions, ensure_ascii=False, indent=2))


def cmd_buy(args):
    """买入股票"""
    trader = THSTrader(args.device)
    result = trader.buy(args.code, args.amount, args.price)

    print("\n" + "="*60)
    print("买入结果")
    print("="*60)
    print(f"  股票代码: {args.code}")
    print(f"  股票名称: {result['stock_name']}")
    print(f"  买入数量: {result['amount']} 股")
    print(f"  买入价格: {result['price']}")
    print(f"  状态: {'✓ 成功' if result['success'] else '✗ 失败'}")
    print(f"  消息: {result['msg']}")
    print("="*60)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0 if result['success'] else 1


def cmd_sell(args):
    """卖出股票"""
    trader = THSTrader(args.device)
    result = trader.sell(args.code, args.amount, args.price)

    print("\n" + "="*60)
    print("卖出结果")
    print("="*60)
    print(f"  股票代码: {args.code}")
    print(f"  股票名称: {result['stock_name']}")
    print(f"  卖出数量: {result['amount']} 股")
    print(f"  卖出价格: {result['price']}")
    print(f"  状态: {'✓ 成功' if result['success'] else '✗ 失败'}")
    print(f"  消息: {result['msg']}")
    print("="*60)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0 if result['success'] else 1


def cmd_withdrawals(args):
    """获取可撤单列表"""
    trader = THSTrader(args.device)
    withdrawals = trader.get_avail_withdrawals()

    print("\n" + "="*60)
    print(f"可撤单列表 (共 {len(withdrawals)} 条)")
    print("="*60)
    for i, w in enumerate(withdrawals, 1):
        print(f"\n{i}. {w['股票名称']} - {w['委托类型']}")
        print(f"   委托价格: {w['委托价格']}")
        print(f"   委托数量: {w['委托数量']} 股")
    print("="*60)

    if args.json:
        print(json.dumps(withdrawals, ensure_ascii=False, indent=2))


def cmd_cancel(args):
    """撤单"""
    trader = THSTrader(args.device)
    result = trader.withdraw(args.name, args.type, args.amount, args.price)

    print("\n" + "="*60)
    print("撤单结果")
    print("="*60)
    print(f"  股票名称: {args.name}")
    print(f"  委托类型: {args.type}")
    print(f"  委托数量: {args.amount} 股")
    print(f"  委托价格: {args.price}")
    print(f"  状态: {'✓ 成功' if result['success'] else '✗ 失败'}")
    print(f"  消息: {result['msg']}")
    print("="*60)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0 if result['success'] else 1


def main():
    parser = argparse.ArgumentParser(
        description='THSTrader - 同花顺模拟炒股自动化交易工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  获取余额:
    %(prog)s balance

  获取持仓:
    %(prog)s position

  买入股票:
    %(prog)s buy --code 002415 --amount 1000 --price 10.0

  卖出股票:
    %(prog)s sell --code 002415 --amount 500 --price 11.0

  查看可撤单:
    %(prog)s withdrawals

  撤单:
    %(prog)s cancel --name 海康威视 --type 买入 --amount 1000 --price 10.0
        """
    )

    parser.add_argument('--device', '-d', default='127.0.0.1:5565',
                       help='设备序列号 (默认: 127.0.0.1:5565)')
    parser.add_argument('--json', '-j', action='store_true',
                       help='输出 JSON 格式')

    subparsers = parser.add_subparsers(dest='command', help='命令')

    # balance 命令
    parser_balance = subparsers.add_parser('balance', help='获取账户余额')
    parser_balance.set_defaults(func=cmd_balance)

    # position 命令
    parser_position = subparsers.add_parser('position', help='获取持仓列表')
    parser_position.set_defaults(func=cmd_position)

    # buy 命令
    parser_buy = subparsers.add_parser('buy', help='买入股票')
    parser_buy.add_argument('--code', '-c', required=True, help='股票代码')
    parser_buy.add_argument('--amount', '-a', type=int, required=True, help='买入数量')
    parser_buy.add_argument('--price', '-p', type=float, required=True, help='买入价格')
    parser_buy.set_defaults(func=cmd_buy)

    # sell 命令
    parser_sell = subparsers.add_parser('sell', help='卖出股票')
    parser_sell.add_argument('--code', '-c', required=True, help='股票代码')
    parser_sell.add_argument('--amount', '-a', type=int, required=True, help='卖出数量')
    parser_sell.add_argument('--price', '-p', type=float, required=True, help='卖出价格')
    parser_sell.set_defaults(func=cmd_sell)

    # withdrawals 命令
    parser_withdrawals = subparsers.add_parser('withdrawals', help='获取可撤单列表')
    parser_withdrawals.set_defaults(func=cmd_withdrawals)

    # cancel 命令
    parser_cancel = subparsers.add_parser('cancel', help='撤单')
    parser_cancel.add_argument('--name', '-n', required=True, help='股票名称')
    parser_cancel.add_argument('--type', '-t', required=True, choices=['买入', '卖出'], help='委托类型')
    parser_cancel.add_argument('--amount', '-a', type=int, required=True, help='委托数量')
    parser_cancel.add_argument('--price', '-p', type=float, required=True, help='委托价格')
    parser_cancel.set_defaults(func=cmd_cancel)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        return 1
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
