# Binance 测试网 API 配置
TESTNET_API_KEY = '7e531f01f53b3774052f522056a47fc584e242b0b38e6e7ccf286278b90a3338'
TESTNET_API_SECRET = 'aaae30371639dc61263ae73d5e70bb643d4bb888e084b33f5a24f4887718248d'

# 交易参数
SYMBOLS = ['ETH/USDT']  # 使用 ETH/USDT 作为交易对
TIMEFRAME_4H = '4h'  # 4小时时间框架
TIMEFRAME_1H = '1h'  # 1小时时间框架

# 策略参数
POSITION_SIZE = 100  # 固定仓位大小为100 USDT

# 均线参数
MA_4H_PERIOD = 12  # 4H的12日均线
MA_1H_PERIOD = 26  # 1H的26日均线

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FILE = 'testnet_trading_log.txt'