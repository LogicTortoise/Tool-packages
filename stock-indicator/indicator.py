import sys
import json
import akshare as ak
import pandas as pd
import pandas_ta as ta
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Get stock indicators')
    parser.add_argument('symbol', type=str, help='Stock symbol (e.g., 000001)')
    parser.add_argument('--days', type=int, default=5, help='Number of recent days to return')
    args = parser.parse_args()

    symbol = args.symbol
    
    # 简单的容错处理，如果用户没输6位，可能要在前面补0？暂时假设用户输入正确
    
    try:
        # 1. 获取个股日线数据 (前复权)
        # 这里的 start_date 设早一点，保证有足够数据计算指标
        start_date = "20240101" 
        current_date = datetime.now().strftime("%Y%m%d")
        
        # akshare 的接口可能会变，目前较稳的是 stock_zh_a_hist
        stock_df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=current_date, adjust="qfq")
        
        if stock_df.empty:
            print(json.dumps({"error": f"No data found for symbol {symbol}"}))
            return

        # 重命名列以适配 pandas_ta (Open, High, Low, Close, Volume)
        stock_df.rename(columns={
            "开盘": "Open", "收盘": "Close", "最高": "High", "最低": "Low", "成交量": "Volume", "日期": "Date"
        }, inplace=True)
        
        # 2. 计算 KDJ
        # pandas_ta 的 kdj 默认返回 K, D, J 三列
        kdj = stock_df.ta.kdj(high="High", low="Low", close="Close", append=True)
        
        # 3. 计算 MACD (顺便送一个)
        stock_df.ta.macd(close="Close", append=True)

        # 4. 整理输出
        # 取最近 N 天
        result_df = stock_df.tail(args.days).copy()
        
        # 修复日期序列化问题：将 Date 列转换为字符串
        result_df['Date'] = result_df['Date'].astype(str)
        
        # 只保留需要的列
        cols_to_keep = ["Date", "Open", "Close", "High", "Low", "Volume"]
        # 动态把计算出来的指标列加进去 (列名通常是 K_9_3, D_9_3, J_9_3 这种格式，我们找含 K/D/J/MACD 的列)
        for col in stock_df.columns:
            if any(x in col for x in ["K_", "D_", "J_", "MACD", "MACDh", "MACDs"]):
                cols_to_keep.append(col)
                
        final_df = result_df[cols_to_keep]
        
        # 转成 JSON
        json_result = final_df.to_dict(orient="records")
        print(json.dumps(json_result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
