# Onymos Online Assesment - Ryan Wong
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue.svg?style=for-the-badge&logo=linkedin&colorB=555)](https://www.linkedin.com/in/ryanwong20)

## Overview

This is an implementation of a real-time stock trading engine for matching stock buys with stock sells. It supports 2 key functions:

- addOrder(): adds a `buy` or `sell` order to the given `ticker`, along with a `quantity` and `price`.
- matchOrder(): matches the `buy` or `sell` order with the given `ticker`.

Multiple threads will be accessing the stock order book at the same time in a randomized simulation.

## Solution

### Map Implementation

The overall idea behind my solution is based on a custom implementation of a hashmap/dictionary, which maps each stock ticker to buy and sell lists. This is done with parallel lists, where `ticker[i]` maps to `buy/sell[i]`. When a stock order is created via `add_order()`, we try to insert it in the buy or sell list at the position of the ticker, if it exists. If we encounter a new ticker, we can append a new ticker and a new buy/sell list in the map.

After the order is added to the ticker, we must match the buy order with the sell order (if possible), or vice versa. This means that `buy_order.price >= sell_order.price`, otherwise it is not possible. That means we want to prioritize the highest buy orders, so all buy orders have to be in decreasing order. Additionally, it means that the sell orders should be in increasing order (we want to match a higher buy order with a lower sell order). If we have 2 orders at the same price, we can order them by the time of their creation.

### Separation of Concern

My solution has been split up into 4 different files:

- `stock_book.py`: contains the `add_order()` and `match_order()` functions as defined in the writeup. `add_order()` takes in a single order object and adds it to the relevant ticker, and then calls `match_order()` to match buy/sell orders for that ticker.
- `stock_map.py`: the underlying data structure behind the stock book. Uses parallel lists to map tickers to their relevant buy/sell listings.
- `order_list.py`: contains the buy and sell lists that are associated with each ticker. All insertion and matching logic is defined here.
- `stock_order.py`: defines a class that encapsulates all relevant details/fields that define a single order, as defined from the writeup. This includes `order_type`, `ticker`, `quantity`, `price`, and `time` (time of creation).
- `simulation.py`: runs a 10-second stock ordering simulation with 10 threads for 10 random pre-defined tickers. Each thread creates a randomized stock order and adds it to the stock book.

The reasoning behind this structure was to separate each level of execution and improve overall readability. Each file and class only handle one aspect of the system, which greatly improves scalibility if different features needed to be implemented. Additionally, I was able to make sure locks were correctly applied only in areas that were necessary.

### Synchronization

In order to properly synchronize my implementation, I used 2 different locks:

- One lock was placed on the map for inserting tickers that do not already exist in the map. This is due to the fact that we could encounter a race condition when 2 threads try to access a ticker that does not already exist, and thus 2 of the same tickers would be created. One thing to note is that the ticker's existence in the list is checked twice; this was to ensure that we only acquire the lock when necessary. If the ticker already exists, we do not need to modify the map and just retuen its index.
- A lock was used on the buy and sell lists for each ticker. This was to ensure that buy/sell orders would not be inserted while we are modifying the list in `match_order()`. If a new order was placed into the map while we were matching orders, it would ruin the behavior of my 2 pointers approach.

### `match_order()` Time Complexity - Two Pointers Approach

In order to write `match_order()` with a time complexity of `O(n)`, I decided to use a two pointers approach. The idea behind this is that we have a pointer at the start of the buy list and another at the start of the sell list. When an order match is valid, `buy_order.price >= sell_order.price`, we can take the smaller quantity of both orders and subtract them, since those orders have been matched. When the quantity reaches 0 for either the buy or sell order, we move to the next in line and check if it is a match again. Once there are no more matches, the indexes we have held will be at the positions where no matches are made yet. The orders behind the index have already been matched, so we delete them from the list. At its worst case, where all items are matched, we go through `n` orders, where `n` is the number of buy/sell orders in the book. So, the runtime comes out to be `O(n)`.

### `add_order()` Time Complexity - Sorting

Following the above logic I have defined in the solution, I sorted the buy orders for each ticker by price in decreasing order, and the sell orders in increasing order. This ensures that the most relevant sell orders match up with the most relevant buy orders. Once I append the new order to its respective list, I sort the entire list, yielding `O(n log n)` time for each insertion where n is the number of orders inside.