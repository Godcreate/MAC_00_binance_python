from config.config import SYMBOL

class OrderExecutor:
    def __init__(self, exchange):
        # 初始化交易所对象
        self.exchange = exchange

    def place_market_order(self, side, amount):
        """
        下市价单
        :param side: 买入或卖出
        :param amount: 交易数量
        :return: 订单信息或None（如果下单失败）
        """
        try:
            order = self.exchange.create_market_order(SYMBOL, side, amount)
            return order
        except Exception as e:
            print(f"Error placing market order: {e}")
            return None

    def place_limit_order(self, side, amount, price):
        """
        下限价单
        :param side: 买入或卖出
        :param amount: 交易数量
        :param price: 限价
        :return: 订单信息或None（如果下单失败）
        """
        try:
            order = self.exchange.create_limit_order(SYMBOL, side, amount, price)
            return order
        except Exception as e:
            print(f"Error placing limit order: {e}")
            return None