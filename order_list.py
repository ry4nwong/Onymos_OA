import threading
from stock_order import StockOrder, OrderType
import time

class OrderList:
    def __init__(self):
        """Creates the order list with buy/sell orders, and a lock for proper synchronization."""
        self.buy_orders = []
        self.sell_orders = []
        self.order_lock = threading.Lock()

    def insert_order(self, order: StockOrder) -> None:
        """Inserts a new order into the buy/sell list."""
        with self.order_lock:
            if order.order_type == OrderType.BUY:
                self.buy_orders.append(order)
                self.buy_orders.sort(key=lambda x: (-x.price, x.time)) # higher price, earlier time
            else:
                self.sell_orders.append(order)
                self.sell_orders.sort(key=lambda x: (x.price, x.time)) # lower price, earlier time

    def match_orders(self) -> None:
        """Matches buy and sell orders in the order list."""
        with self.order_lock:    
            # 2 pointers approach
            buy_index, sell_index = 0, 0
            while buy_index < len(self.buy_orders) and sell_index < len(self.sell_orders):
                buy_order = self.buy_orders[buy_index] # max buy price
                sell_order = self.sell_orders[sell_index] # min sell price

                # valid trade to be made
                if buy_order.price >= sell_order.price:
                    # update quantities
                    quantity = min(buy_order.quantity, sell_order.quantity)
                    print(f"Matched {quantity} shares of {buy_order.ticker} at ${sell_order.price}")

                    # update buy order
                    buy_order.quantity -= quantity
                    if buy_order.quantity == 0:
                        buy_index += 1

                    # update sell order
                    sell_order.quantity -= quantity
                    if sell_order.quantity == 0:
                        sell_index += 1
                else:
                    break # no valid trades available

            # delete matched orders
            del self.buy_orders[:buy_index]
            del self.sell_orders[:sell_index]