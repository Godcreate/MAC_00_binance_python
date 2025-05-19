import time
import pandas as pd
from execution.testnet_order_executor import TestnetOrderExecutor
from strategy.multi_strategy import MultiStrategy
from strategy.BinanceFuture_4H_1H_2 import DMRCrossoverStrategy
from utils.logger import setup_logger
import os
from data.data_fetcher import DataFetcher
from datetime import datetime, timedelta

def update_data(fetcher, symbol, filename):
    """更新市场数据"""
    df = fetcher.get_historical_data(symbol, '1h', limit=1000)
    if df is not None:
        fetcher.save_data_to_csv(df, filename)
        return df
    return None

def main():
    logger = setup_logger()
    
    # 初始化数据获取器和交易执行器
    fetcher = DataFetcher()
    order_executor = TestnetOrderExecutor()
    multi_strategy = MultiStrategy(order_executor)
    
    # 设置交易对和数据文件路径
    # main.py ：主程序文件，数据路径已经正确设置为Mac格式：data_dir = '/Users/wangjinfang/Desktop/DEMO/DEMO_00_binance_python/data'
    symbol = 'ETH/USDT'
    data_dir = '/Users/wangjinfang/Desktop/DEMO/DEMO_00_binance_python/data'
    os.makedirs(data_dir, exist_ok=True)
    data_path = f'{data_dir}/ETH_USDT_data.csv'
    
    logger.info("Starting testnet trading bot with ETH/USDT DMR strategy")
    
    try:
        while True:
            current_time = datetime.now()
            
            # 更新市场数据
            df = update_data(fetcher, symbol, data_path)
            if df is None:
                logger.error("Failed to update market data")
                time.sleep(60)  # 等待1分钟后重试
                continue
                
            logger.info(f"Updated market data at {current_time}")
            
            # 创建并执行策略
            dmr_strategy = DMRCrossoverStrategy(df, order_executor)
            multi_strategy.add_strategy(dmr_strategy)
            
            try:
                multi_strategy.execute_strategies()
                logger.info("Strategy execution completed")
            except Exception as e:
                logger.error(f"Strategy execution error: {e}")
            
            # 清空策略列表，准备下一轮
            multi_strategy.strategies.clear()
            
            # 计算等待时间到下一个小时
            next_hour = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            wait_seconds = (next_hour - current_time).total_seconds()
            
            logger.info(f"Waiting {wait_seconds:.0f} seconds for next update")
            time.sleep(wait_seconds)
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Bot stopped")

if __name__ == "__main__":
    main()