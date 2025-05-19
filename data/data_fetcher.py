import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

import ccxt
import pandas as pd
from config.testnet_config import (
    TESTNET_API_KEY, TESTNET_API_SECRET, 
    SYMBOLS, TIMEFRAME_4H, TIMEFRAME_1H
)

class DataFetcher:
    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': TESTNET_API_KEY,
            'secret': TESTNET_API_SECRET,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
                'adjustForTimeDifference': True,
                'testnet': True  # 启用测试网
            }
        })

    def get_historical_data(self, symbol, timeframe, limit=1000):
        """
        获取历史K线数据
        """
        try:
            print(f"Fetching {timeframe} data for {symbol}...")
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            print(f"Successfully fetched {len(df)} rows of {timeframe} data for {symbol}")
            return df
        except Exception as e:
            print(f"Error fetching {timeframe} data for {symbol}: {str(e)}")
            return None

    def save_data_to_csv(self, df, filename):
        """将数据保存到CSV文件"""
        if df is not None:
            # 确保目录存在
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            df.to_csv(filename)
            print(f"Data saved to {filename}")
            return True
        else:
            print(f"No data to save to {filename}")
            return False

def setup_data_directory():
    """设置数据目录"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    
    # 确保数据目录存在
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def main():
    # 设置数据目录
    data_dir = setup_data_directory()
    print(f"Data directory: {data_dir}")
    
    fetcher = DataFetcher()
    
    for symbol in SYMBOLS:
        # 构建文件名
        filename = data_dir / f"{symbol.split('/')[0]}_USDT_data.csv"
        
        # 获取1小时和4小时数据
        df_1h = fetcher.get_historical_data(symbol, TIMEFRAME_1H, limit=1000)
        
        if df_1h is not None:
            # 保存数据
            if fetcher.save_data_to_csv(df_1h, filename):
                print(f"Successfully saved data for {symbol}")
            else:
                print(f"Failed to save data for {symbol}")
        else:
            print(f"Failed to fetch data for {symbol}")

if __name__ == "__main__":
    main()