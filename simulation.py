import threading
import time
import random
from stock_book import StockBook, StockOrder
from stock_map import OrderType

# List of random tickers for simulation
TICKERS = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "FB", "NVDA", "INTC", "CSCO", "ADBE"]

# Create stock book
stock_book = StockBook()

# Stop event for threads
stop_event = threading.Event()

def random_order(thread):
    while not stop_event.is_set():
        order_type = OrderType.BUY if random.random() < 0.5 else OrderType.SELL
        ticker = random.choice(TICKERS)
        quantity = random.randint(1, 100)
        price = round(random.uniform(100, 200), 2)

        stock_book.add_order(StockOrder(order_type, ticker, quantity, price, time.time()))

        print(f"Thread {thread} inserted order for {ticker}.")

        time.sleep(random.uniform(0.1, 1.0))

# Runs 10 threads
threads = []
for i in range(10):
    thread = threading.Thread(target=random_order, args=(i,))
    threads.append(thread)
    thread.start()
    
# Run simulation for 10 seconds
time.sleep(10)
stop_event.set()

# Stop threads
for thread in threads:
    thread.join(timeout=1)

# Final state of the order book
print("\n\n---------------- Order Book After Simulation ----------------\n\n")
for ticker in TICKERS:
    order = stock_book.stock_map.get_orders(ticker)
    buy_orders = order.buy_orders
    sell_orders = order.sell_orders

    print(f"\n\n---------------- {ticker} Buy Orders: ----------------\n\n")
    for order in buy_orders:
        print(f"Quantity: {order.quantity}, Price: {order.price}")

    print(f"\n\n---------------- {ticker} Sell Orders: ----------------\n\n")
    for order in sell_orders:
        print(f"Quantity: {order.quantity}, Price: {order.price}")