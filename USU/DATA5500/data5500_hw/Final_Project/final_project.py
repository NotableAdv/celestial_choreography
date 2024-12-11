# importing libraries
import pandas as pd
from alpaca_trade_api import REST, TimeFrame
from datetime import datetime, timedelta
import os
import json
import requests

# connection to the Alpaca Paper Trading API
api_key = 'PKOB9ZS16PJHYP43DHFP'
secret_key = 'rOxbWJab3SjAOfQLu61Z7JOlmj1wfnNM6Zc2OfPa' 
base_url = 'https://paper-api.alpaca.markets'
api = REST(api_key, secret_key, base_url=base_url)

# creating basis for file storage not hard coded
curr_dir = os.path.dirname(__file__)  # Final_Project directory
data_dir = os.path.join(curr_dir, "data")  # Data folder inside Final_Project
results_file = os.path.join(curr_dir, 'results.json') # The results.json file

# stocks we will track/trade
tickers = ["AAPL", "ADBE", "BBY", "DPZ", "GOOG", "MCD", "SBUX", "TGT", "ULTA", "WMT"]

# requesting the prices from Alpaca
def data_pull(ticker, start_date, end_date):

    # try to pull the data
    try:
        print(f"Fetching data for {ticker} from {start_date} to {end_date}...")

        # the api saves the prices in bars
        bars = api.get_bars(
            ticker,
            TimeFrame.Day,
            start=start_date,
            end=end_date,
            feed='iex'
        ).df

        bars['ticker'] = ticker  # column for the stock ticker
        bars.index = pd.to_datetime(bars.index)  # timestamps need to be datetime objects

        # file path to save the csv to
        filepath = os.path.join(data_dir, f'{ticker}.csv')

        # merge files if one already exists by that name - to help with updating the data
        if os.path.exists(filepath):

            # the file for the stock prices
            existing_data = pd.read_csv(filepath)

            # specify format to ensure consistency
            existing_data['timestamp'] = pd.to_datetime(existing_data['timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

            # drop any empty rows
            existing_data = existing_data.dropna(subset=['timestamp'])

            # only concatenate if both dataframes are non-empty
            if not existing_data.empty and not bars.empty:

                # drop duplicates to ensure updating doesn't readd all data
                bars = pd.concat([existing_data, bars]).drop_duplicates(subset='timestamp')

            # only use the new data if there is not existing data
            elif not existing_data.empty:
                bars = existing_data

        # save to CSV the prices to the csv file
        bars.to_csv(filepath, index_label='timestamp')
        print(f"Data saved to {filepath}.")
        print()

    # read error if the data pull doesn't go through    
    except Exception as e:
        print(f"An error occurred during the data pull: {e}")

# Mean Reversion Strategy
def meanReversionStrategy(prices):

    # setting variables
    i = 0
    buy = 0
    sell = 0
    first_buy = 0
    total_profit = 0
    signal = "no"

    # takes the 5 most recent prices and checks if they are higher enough or low enough to send a buy or sell signal  
    for price in prices:
        if i >= 5:
            current_price = price
            average = (prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5]) / 5
        
            # Buying signal
            if current_price < (average * 0.98):
                buy = current_price
                signal = "buy"
                profit = sell - buy
                total_profit += profit
                if first_buy == 0:
                    first_buy = current_price
                sell = 0 # reset sell
            
            # Selling signal
            elif current_price > (average * 1.02):
                sell = current_price
                signal = "sell"
                profit = sell - buy
                total_profit += profit
                buy = 0  # reset buy
            
            # otherwise no signal is sent
            else: 
                signal = "no"

        # move to the next price    
        i += 1    

    # return the total profit and profit percentage
    final_profit_percentage = (total_profit / first_buy) * 100
    return(total_profit, final_profit_percentage, signal)

# Simple Moving Average Strategy
def simpleMovingAverageStrategy(prices):

    # setting variables
    i = 0
    buy = 0
    sell = 0
    first_buy = 0
    total_profit = 0
    signal = "no"
    
    # takes the 5 most recent prices and sends a buy or sell signal if the average is higher or lower than the current average
    for price in prices:
        if i >= 5:
            current_price = price
            average = (prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5]) / 5
        
            # Buying signal
            if current_price < average:
                buy = current_price
                signal = "buy"
                profit = sell - buy
                total_profit += profit
                if first_buy == 0:
                    first_buy = current_price
                sell = 0 # reset sell
            
            # Selling signal
            elif current_price > average:
                sell = current_price
                signal = "sell"
                profit = sell - buy
                total_profit += profit
                buy = 0  # reset buy
            
            # otherwise no signal is sent
            else: 
                signal = "no"

        # move to the next price     
        i += 1    

    # return the total profit and profit percentage
    final_profit_percentage = (total_profit / first_buy) * 100
    return(total_profit, final_profit_percentage, signal)

# Bollinger Bands Strategy
def bollingerBandsStrategy(prices):

    # setting variables
    i = 0
    buy = 0
    sell = 0
    first_buy = 0
    total_profit = 0
    signal = "no"

    # takes the 5 most recent prices and sends a buy or sell signal, sells stocks with a lower price and buys high compared to average
    for price in prices:
        if i >= 5:
            current_price = price
            average = (prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5]) / 5
        
            # Buying signal
            if current_price > (average * 1.05):
                buy = current_price
                signal = "buy"
                profit = sell - buy
                total_profit += profit
                if first_buy == 0:
                    first_buy = current_price
                sell = 0 # reset sell
            
            # Selling signal
            elif current_price < (average * 0.95):
                sell = current_price
                signal = "sell"
                profit = sell - buy
                total_profit += profit
                buy = 0  # reset buy
            
            # otherwise no signal is sent
            else: 
                signal = "no"

        # move to the next price             
        i += 1    

    # return the total profit and profit percentage
    final_profit_percentage = (total_profit / first_buy) * 100
    return(total_profit, final_profit_percentage, signal)

# function for submitted an order with the Alpaca paper API
def place_order(symbol, side):
    try:
        # Place an order with a qty of 1
        order = api.submit_order(
            symbol = symbol,
            qty = 1,
            side = side,
            type = 'market',
            time_in_force = 'gtc'
        )
        print(f"Order submitted: {side} 1 {symbol} stock")
        return order
    
    # if the order doesn't go through, output the error
    except Exception as e:
        print(f"Error placing order: {e}")

# Saving results in a json
def saveResults(results):
    file = open(results_file, "w")
    json.dump(results, file, indent=4)

# Run the data pull for all tickers from the beginning of 2024 to current date
for ticker in tickers:
    filepath = results_file
    end_date = datetime.now().strftime('%Y-%m-%d')
    data_pull(ticker, '2024-01-01', end_date)

# dictionary setup
results = {}
profits = {}

# Looping through each stock
for ticker in tickers:

    # Loading prices from the CSV file
    price_file = open(os.path.join(data_dir, ticker + ".csv"), "r")
    lines = price_file.readlines()
    prices = []

    # add the prices to a dictionary
    for line in lines:
        if not line.startswith("timestamp"):  # skip the header
            price = float(line.split(",")[1])  # index 1 corresponds to 'close'
            prices.append(price)
    
    #print(prices) # checking the prices added to the dictionary

    # run Mean Reversion strategy
    profit, returns, signal = meanReversionStrategy(prices)
    results[ticker + "_mr_profit"] = round(profit, 2)
    results[ticker + "_mr_returns"] = round(returns, 2)
    profits[ticker + "_mr_profit"] = round(profit, 2)

    # if the strategy returns a signal and order will be placed    
    if signal == "buy" or signal == "sell":
        print(f"MR: You should {signal} {ticker} today.")
        place_order(ticker, signal)
        print()
    
    # run Simple Moving Average strategy
    profit, returns, signal = simpleMovingAverageStrategy(prices)
    results[ticker + "_sma_profit"] = round(profit, 2)
    results[ticker + "_sma_returns"] = round(returns, 2)
    profits[ticker + "_sma_profit"] = round(profit, 2)

    # if the strategy returns a signal and order will be placed    
    if signal == "buy" or signal == "sell":
        print(f"SMA: You should {signal} {ticker} today.")
        place_order(ticker, signal)
        print()
    
    # run Bollinger Bands strategy
    profit, returns, signal = bollingerBandsStrategy(prices)
    results[ticker + "_bb_profit"] = round(profit, 2)
    results[ticker + "_bb_returns"] = round(returns, 2)
    profits[ticker + "_bb_profit"] = round(profit, 2)
    
    # if the strategy returns a signal and order will be placed
    if signal == "buy" or signal == "sell":
        print(f"BB: You should {signal} {ticker} today.")
        place_order(ticker, signal)
        print()

# Finding the highest profit and adding it to the results
max_profit = max(profits, key=profits.get)
largest = "Highest profit"
results[largest] = (max_profit, profits[max_profit])

# Printing the highest profit to the console
print(f"Since the start of 2024, the stock and strategy that made the most profit is {max_profit}: ${profits[max_profit]:.2f}")

# Saving data to add results to the JSON file
saveResults(results)
