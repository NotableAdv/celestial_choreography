import alpaca_trade_api as tradeapi

# Set up Alpaca API
ALPACA_API_KEY = 'PK0UIH8MUPY38EIYNEF5'
ALPACA_API_SECRET = 'yaqdUMPcwP7tzFI03hCi3axRUdX341peYlmVcvqj'
API_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_API_SECRET, API_URL, api_version='v2')

# Define paths
largest_path = (['bch', 'btc', 'link', 'yfi', 'dot', 'ltc', 'eth'], ['eth', 'btc', 'link', 'yfi', 'dot', 'ltc', 'bch'])

# Function to execute a trade order
def execute_order(symbol, qty, side, order_type='market', time_in_force='gtc'):
    try:
        # Place an order
        order = api.submit_order(
            symbol= symbol.upper(),
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force
        )
        print(f"Order submitted: {side} {qty} {symbol}")
        return order
    except Exception as e:
        print(f"Error placing order: {e}")

# Arbitrage strategy to buy/sell from the two paths
def execute_arbitrage(largest_path):
    p1, p2 = largest_path

    print(f"Attempting arbitrage between {p1} and {p2}")

    # Iterate through path_1 and path_2 to execute individual orders
    qty = 1

    # Loop through each symbol in path_1
    for p in p1:
        symbol_1 = f'{p}USD'  # Ensure the symbol is like 'bchUSD'
        print(f"Placing buy order for {symbol_1} (Buy)")
        execute_order(symbol_1, qty, 'buy')

    # Loop through each symbol in path_2
    for p in p2:
        symbol_2 = f'{p}USD'  # Ensure the symbol is like 'ethUSD'
        print(f"Placing sell order for {symbol_2} (Sell)")
        execute_order(symbol_2, qty, 'sell')

# Execute the arbitrage
execute_arbitrage(largest_path)