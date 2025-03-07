from stock_map import StockMap
from stock_order import OrderType, StockOrder

class StockBook:
    def __init__(self):
        """Creates the stock book with tickers, mapped to buy/sell orders."""
        self.stock_map = StockMap()

    def add_order(self, order: StockOrder) -> None:
        """Adds a new order to the stock book."""

        # Insert order into stock map
        self.stock_map.insert_order(order)

        # Match orders
        self.match_order(order.ticker)

    def match_order(self, ticker: str) -> None:
        """Matches buy and sell orders for a given ticker."""

        self.stock_map.get_orders(ticker).match_orders()
