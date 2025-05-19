import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config.testnet_config import POSITION_SIZE

class DMRCrossoverStrategy:
    def __init__(self, df, order_executor, commission=0.001):
        """
        初始化策略
        df: DataFrame，包含 'high', 'low', 'close' 的OHLCV数据
        order_executor: 交易执行器
        commission: 交易手续费率
        """
        self.df = df
        self.order_executor = order_executor
        self.commission = commission
        self.positions = pd.DataFrame(index=df.index)
        
    def calculate_dmr(self):
        """计算DMR指标"""
        # 1. 计算中间价
        self.df['dmr_midprice'] = (self.df['high'] + self.df['low']) / 2
        
        # 2. 计算中间价比率
        self.df['dmr_ratio'] = self.df['dmr_midprice'] / self.df['dmr_midprice'].shift(1)
        
        # 3-5. 计算不同周期的移动平均
        self.df['dmr_avg6'] = self.df['dmr_ratio'].rolling(window=6).mean() - 1
        self.df['dmr_avg12'] = self.df['dmr_ratio'].rolling(window=12).mean() - 1
        self.df['dmr_avg26'] = self.df['dmr_ratio'].rolling(window=26).mean() - 1
        
    def resample_data(self):
        """重采样数据到4H和1H时间周期"""
        # 4H 数据重采样
        self.df_4h = self.df.resample('4h').agg({
            'high': 'max',
            'low': 'min',
            'dmr_avg12': 'last'
        }).dropna()
        
        # 1H 数据重采样
        self.df_1h = self.df.resample('1h').agg({
            'high': 'max',
            'low': 'min',
            'dmr_avg26': 'last'
        }).dropna()
        
    def generate_signals(self):
        """生成交易信号"""
        # 4H 策略信号
        self.df_4h['signal_4h'] = 0
        # 当4H的12日均线数值由负值转为正值时开多
        self.df_4h.loc[(self.df_4h['dmr_avg12'].shift(1) < 0) & (self.df_4h['dmr_avg12'] > 0), 'signal_4h'] = 1
        # 当4H的12日均线数值由正值转为负值时开空
        self.df_4h.loc[(self.df_4h['dmr_avg12'].shift(1) > 0) & (self.df_4h['dmr_avg12'] < 0), 'signal_4h'] = -1
        
        # 1H 策略信号
        self.df_1h['signal_1h'] = 0
        # 当1H的26日均线数值由负值转为正值时开多
        self.df_1h.loc[(self.df_1h['dmr_avg26'].shift(1) < 0) & (self.df_1h['dmr_avg26'] > 0), 'signal_1h'] = 1
        # 当1H的26日均线数值由正值转为负值时开空
        self.df_1h.loc[(self.df_1h['dmr_avg26'].shift(1) > 0) & (self.df_1h['dmr_avg26'] < 0), 'signal_1h'] = -1
        
    def execute_trades(self):
        """执行交易策略"""
        # 只获取最新的信号
        if len(self.df_4h) > 0:
            latest_4h_signal = self.df_4h['signal_4h'].iloc[-1]  # 获取4H最新信号
            if latest_4h_signal == 1:  # 最新4H信号为开多
                self.order_executor.close_position('ETH/USDT', 'LONG')
                self.order_executor.open_long('ETH/USDT', POSITION_SIZE)  # 固定100USDT
                print(f"4H Strategy: Opening LONG position with {POSITION_SIZE} USDT")
            elif latest_4h_signal == -1:  # 最新4H信号为开空
                self.order_executor.close_position('ETH/USDT', 'SHORT')
                self.order_executor.open_short('ETH/USDT', POSITION_SIZE)  # 固定100USDT
                print(f"4H Strategy: Opening SHORT position with {POSITION_SIZE} USDT")

        if len(self.df_1h) > 0:
            latest_1h_signal = self.df_1h['signal_1h'].iloc[-1]  # 获取1H最新信号
            if latest_1h_signal == 1:  # 最新1H信号为开多
                self.order_executor.close_position('ETH/USDT', 'LONG')
                self.order_executor.open_long('ETH/USDT', POSITION_SIZE)  # 固定100USDT
                print(f"1H Strategy: Opening LONG position with {POSITION_SIZE} USDT")
            elif latest_1h_signal == -1:  # 最新1H信号为开空
                self.order_executor.close_position('ETH/USDT', 'SHORT')
                self.order_executor.open_short('ETH/USDT', POSITION_SIZE)  # 固定100USDT
                print(f"1H Strategy: Opening SHORT position with {POSITION_SIZE} USDT")
        
    def run_strategy(self):
        """运行完整策略"""
        self.calculate_dmr()
        self.resample_data()
        self.generate_signals()
        self.execute_trades()
        return self.df

if __name__ == "__main__":
    pass