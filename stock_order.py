from enum import Enum
import time

class OrderType(Enum):
    BUY = 1
    SELL = 2

class StockOrder:
    def __init__(self, order_type: OrderType, ticker: str, quantity: int, price: float, time: time):
        """Defines a single order to buy or sell a stock at a certain quantity and price."""
        self.order_type = order_type
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.time = time