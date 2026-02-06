import sys
import os
# Ensure the current directory is in python path to find 'ths'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ths.trader import THSTrader

def main():
    print("Initializing THSTrader...")
    # Use the specific device serial
    trader = THSTrader(serial="127.0.0.1:5565")
    
    print("Testing buy...")
    # 601398 (ICBC), 10000 shares, at 7.30
    print("Pre-checks passed, invoking buy()...")
    sys.stdout.flush()
    result = trader.buy("601398", "10000", "7.30")
    print(f"Buy result: {result}")

if __name__ == "__main__":
    main()
