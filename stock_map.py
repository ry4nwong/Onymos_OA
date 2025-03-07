import threading
from stock_order import StockOrder, OrderType
from order_list import OrderList

class StockMap:
    def __init__(self):
        """Creates the stock map with tickers mapped to buy/sell orders, and a lock."""
        self.map_lock = threading.Lock()
        self.tickers = []
        self.orders = []

    def get_ticker_index(self, ticker: str) -> int:
        """Returns the index of the buy/sell orders for a given ticker, or creates a new one if it doesn't exist."""
        # Need to add ticker if not already present
        if ticker not in self.tickers:
            with self.map_lock:
                # Check again, a previous thread might have added the ticker
                if ticker not in self.tickers:
                    self.tickers.append(ticker)
                    self.orders.append(OrderList())
                    return len(self.tickers) - 1
                else:
                    return self.tickers.index(ticker)
        
        return self.tickers.index(ticker)
    
    def get_orders(self, ticker: str) -> OrderList:
        """Returns the buy and sell orders for a given ticker."""
        ticker_index = self.get_ticker_index(ticker)
        return self.orders[ticker_index]
    
    def insert_order(self, order: StockOrder) -> None:
        """Inserts a new order into buy/sell list for a given order."""
        ticker_index = self.get_ticker_index(order.ticker)

        self.orders[ticker_index].insert_order(order)
