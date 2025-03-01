import alpaca_trade_api as tradeapi
import time
from alpaca_trade_api.rest import REST, TimeFrame

ALPACA_API_KEY = 'PK0UIH8MUPY38EIYNEF5'
ALPACA_API_SECRET = 'yaqdUMPcwP7tzFI03hCi3axRUdX341peYlmVcvqj'
API_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_API_SECRET, API_URL, api_version='v2')

# Define the trade path
trade_path = ['ETH', 'BTC', 'LINK', 'LTC', 'DOT']

# Start with an initial amount in USD (e.g., $1000)
initial_balance = 1000000

# Function to execute a trade
def execute_trade(symbol, amount, trade_type='buy'):
    try:
        if trade_type == 'buy':
            order = api.submit_order(
                symbol=symbol,
                qty=None,  # Not fixed; based on amount and current price
                notional=amount,
                side='buy',
                type='market',
                time_in_force='day'
            )
        else:  # Sell
            current_price = api.get_latest_trade(symbol).price
            qty = amount / current_price
            order = api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='day'
            )
        time.sleep(1)  # Avoid rate limit
        return order
    except Exception as e:
        print(f"Error with {trade_type} order for {symbol}: {e}")
        return None


# Sequential trading
current_balance = initial_balance

# Ensure you buy the first asset
first_symbol = trade_path[0]
print(f"Buying the first asset: {first_symbol}")
buy_order = execute_trade(first_symbol, current_balance, trade_type='buy')
if not buy_order:
    print("Initial buy trade failed. Exiting.")
    exit()

print(f"Bought {first_symbol}. Current balance: {current_balance:.2f}")

for i in range(len(trade_path) - 1):
    from_symbol = trade_path[i]
    to_symbol = trade_path[i + 1]

    print(f"Trading {from_symbol} → {to_symbol}")
    
    # Sell 'from_symbol' to USD
    sell_order = execute_trade(from_symbol, current_balance, trade_type='sell')
    if not sell_order:
        print("Trade failed. Exiting.")
        break

    time.sleep(5)  # Add a delay to avoid wash trade detection

    # Update balance
    sell_price = api.get_latest_trade(from_symbol).price
    current_balance *= sell_price
    print(f"Sold {from_symbol}. New balance in USD: ${current_balance:.2f}")

    # Buy 'to_symbol' with updated USD balance
    buy_order = execute_trade(to_symbol, current_balance, trade_type='buy')
    if not buy_order:
        print("Trade failed. Exiting.")
        break

    time.sleep(5)  # Add a delay to avoid wash trade detection

    # Update balance
    buy_price = api.get_latest_trade(to_symbol).price
    current_balance /= buy_price
    print(f"Bought {to_symbol}. New balance: {current_balance:.8f} {to_symbol}")

# Final balance
print(f"Final balance after trading: {current_balance:.8f} {trade_path[-1]}")

