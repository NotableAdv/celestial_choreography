import alpaca_trade_api as tradeapi
import time

ALPACA_API_KEY = 'PK0UIH8MUPY38EIYNEF5'
ALPACA_API_SECRET = 'yaqdUMPcwP7tzFI03hCi3axRUdX341peYlmVcvqj'
API_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_API_SECRET, API_URL, api_version='v2')

# List of currencies to trade in sequence (all USD pairs)
currencies = ['ethUSD', 'btcUSD', 'linkUSD', 'ltcUSD', 'dotUSD']

# Function to get the account balance in USD
def get_balance():
    account = api.get_account()
    cash = float(account.cash)  # Available cash balance in USD
    return cash

# Function to fetch the current price of a symbol
def get_current_price(symbol):
    barset = api.get_latest_trade(symbol)
    return float(barset.price)

# Function to place a market order
def place_order(symbol, qty, side='buy'):
    try:
        print(f"Placing {side} order for {qty} units of {symbol}...")
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        print(f"Order placed: {order}")
        return order
    except Exception as e:
        print(f"Error placing order: {e}")

# Sequentially trade each currency in the list
def execute_trades():
    # Get initial balance in USD
    balance = get_balance()
    print(f"Starting balance: ${balance}")

    for i in range(len(currencies)):
        current_currency = currencies[i]

        # Get the current price of the currency
        current_price = get_current_price(current_currency)

        if i == 0:
            # First iteration: Buy the first currency using the entire balance
            amount = balance / current_price  # How much of the first currency to buy
            print(f"Buying {amount} of {current_currency} at ${current_price} each.")
            place_order(current_currency, amount, side='buy')

        else:
            # For subsequent iterations:
            # Step 1: Sell the previous currency for USD
            previous_currency = currencies[i - 1]
            sell_price = get_current_price(previous_currency)
            print(f"Selling {amount} of {previous_currency} at ${sell_price} each.")
            balance = amount * sell_price  # Update balance after selling
            place_order(previous_currency, amount, side='sell')

            # Step 2: Buy the next currency using the updated balance
            amount = balance / current_price  # Calculate how much of the next currency to buy
            print(f"Buying {amount} of {current_currency} at ${current_price} each.")
            place_order(current_currency, amount, side='buy')

        # Optional: Add a delay to avoid rate limits
        time.sleep(1)

    print(f"\nCompleted trading sequence. Final balance in {currencies[-1]}: {amount}")

# Start trading
execute_trades()
