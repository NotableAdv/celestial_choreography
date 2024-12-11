
# importing libraries
import os
import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations
import alpaca_trade_api as tradeapi
import csv
from datetime import datetime
import time


# function to calculate the weight of a path by multiplying the weights together
def calculate_path_weight(g, path):
    path_weight = 1
    for i in range(len(path) - 1):
        path_weight *= g[path[i]][path[i+1]]['weight']
    return path_weight

# function to find all the paths, print them, and find the paths with the smallest and largest factors
def find_paths(g):
    # setting up variables
    smallest_path = []
    largest_path = []
    smallest_factor = 100
    largest_factor = -100

    # for the first node to the last node we're searching through if it has paths, find all the paths in both orders
    for start, end in permutations(g.nodes, 2):
        if nx.has_path(g, start, end):
            forward_paths = list(nx.all_simple_paths(g, start, end))
            reverse_paths = list(nx.all_simple_paths(g, end, start))

            # if the nodes have paths that can go both ways
            if forward_paths and reverse_paths:

                # calculate the weight of forward paths
                for forward_path in forward_paths:
                    forward_weight = calculate_path_weight(g,forward_path)

                    # calculate the weight of reverse paths
                    for reverse_path in reverse_paths:
                        reverse_weight = calculate_path_weight(g,reverse_path)

                        # multiply the weights to get the arbitrage factor
                        factor = forward_weight * reverse_weight

                        # if the factor is the current smallest, make it the smallest and save it's path
                        if factor < smallest_factor:
                            smallest_factor = factor
                            smallest_path = (forward_path, reverse_path)

                        # if the factor is the current largest, make it the largest and save it's path    
                        if factor > largest_factor:
                            largest_factor = factor
                            largest_path = (forward_path, reverse_path)

    # return the result information
    return smallest_factor, largest_factor, smallest_path, largest_path                

# Function to execute a trade order
def execute_order(symbol, qty, side, order_type='market', time_in_force='gtc'):
    # Execute a market order to buy or sell a specific asset (stock/ETF)
    try:
        if side == 'buy':
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side='buy',
                type=order_type,
                time_in_force=time_in_force
            )
            print(f"Order submitted: {side} {qty} {symbol}")
        elif side == 'sell':
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type=order_type,
                time_in_force=time_in_force
            )
            print(f"Order submitted: {side} {qty} {symbol}")
    except Exception as e:
        print(f"Error placing order for {symbol}: {e}")


def arbitrage_path_finder(largest_path):
    path1, path2 = largest_path
    print(f"Attempting arbitrage between {path1[0]} and {path2[0]}")

    # Append elements from list2 starting from the second element
    arbitrage_path = path1 + path2[1:]

    return arbitrage_path


def get_available_assets():
    # Get a list of available assets (stocks) that you can trade
    assets = api.list_assets()
    available_assets = [asset.symbol for asset in assets if asset.tradable]
    return available_assets

def check_asset_available(from_symbol, to_symbol):
    # Get the list of available assets and check if both are available
    available_assets = get_available_assets()
    return from_symbol in available_assets and to_symbol in available_assets

def execute_arbitrage(arbitrage_path):
    qty = 1  # Example trade quantity

    for i in range(len(arbitrage_path) - 1):
        from_symbol = arbitrage_path[i].upper()
        to_symbol = arbitrage_path[i + 1].upper()

        print(f"Attempting to arbitrage between {from_symbol} and {to_symbol}")

        # Check if both assets are available for trading
        if check_asset_available(from_symbol, to_symbol):
            print(f"Placing buy order for {from_symbol}")
            execute_order(from_symbol, qty, 'buy')

            time.sleep(5)  # Wait for the buy to complete

            print(f"Placing sell order for {from_symbol}")
            execute_order(from_symbol, qty, 'sell')

            time.sleep(5)  # Wait before placing the next order

            print(f"Placing buy order for {to_symbol}")
            execute_order(to_symbol, qty, 'buy')

            time.sleep(5)  # Wait for the buy to complete

            print(f"Placing sell order for {to_symbol}")
            execute_order(to_symbol, qty, 'sell')

        else:
            # Fallback to USD-based trading if the direct pair isn't available
            print(f"Direct pair {from_symbol}/{to_symbol} not available. Falling back to USD.")
            
            # First, sell from_symbol to USD
            print(f"Placing sell order for {from_symbol} to USD")
            execute_order(from_symbol, qty, 'sell')

            time.sleep(5)  # Wait before buying the next asset

            # Then, buy to_symbol from USD
            print(f"Placing buy order for {to_symbol} from USD")
            execute_order(to_symbol, qty, 'buy')

# file the cyrpto currencies are listed in
curr_dir = os.path.dirname(__file__)
file_path = os.path.join(curr_dir, "crypto_ids.txt")
data_folder = os.path.join(curr_dir, "data")

timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M")

# Create the filename
filename = os.path.join(data_folder, f"currency_pair_{timestamp}.txt")

ALPACA_API_KEY = 'PK0UIH8MUPY38EIYNEF5'
ALPACA_API_SECRET = 'yaqdUMPcwP7tzFI03hCi3axRUdX341peYlmVcvqj'
API_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_API_SECRET, API_URL, api_version='v2')

# read the currencies from file
currencies = []
currency_map = {}
with open(file_path, "r") as file:
    for line in file:
        id, vs = line.strip().split(",")
        currencies.append(vs)
        currency_map[vs] = id

# initialize directional graph
g = nx.DiGraph()
edges = []

# url to pull the data in from the API
base_url_template = 'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={vs_currencies}'

# batch size for sending all requests to the API at once
batch_size = 50

# split currencies into batches
currency_batches = [currencies[i:i + batch_size] for i in range(0, len(currencies), batch_size)]

# call the api for the exchange rates in batches
for batch in currency_batches:
    ids = ','.join([currency_map[sym] for sym in batch])
    vs_currencies = ','.join(currencies)  # Compare against all currencies
    url = base_url_template.format(ids=ids, vs_currencies=vs_currencies)
    
    # if the data will pull from the API
    try:
        # make the API request
        req = requests.get(url)
        req.raise_for_status()  # Raise error for HTTP issues
        api_data = req.json()
        
        # add the node info from the API
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["currency_from", "currency_to", "exchange_rate"])  # Header

            # Add data while building the graph
            for c1, c2 in permutations(currencies, 2):
                if c1 != c2 and c2 in api_data[currency_map[c1]]:
                    rate = api_data[currency_map[c1]][c2]
                    g.add_edge(c1, c2, weight=rate)

                    # Write to CSV file
                    writer.writerow([c1, c2, rate])

    # if the data won't pull from the API
    except Exception as e:
        print(f"Error fetching data for batch {batch}: {e}")

# trying to call the function for outputting results
try:
    smallest_factor, largest_factor, smallest_path, largest_path = find_paths(g) 
    print()
    print('Smallest Path Weight Factor:', smallest_factor) # worst trade to make right then
    print('Paths:', smallest_path)
    print('Largest Path Weight Factor:', largest_factor) # best trade to make right then
    print('Paths:', largest_path)

    execute_arbitrage(arbitrage_path_finder(largest_path))

# in case there is an error for finding paths    
except:
    print(f"Error during path finding: {e}")


# printing a graph of the currency exchange rates
curr_dir = os.path.dirname(__file__) # get the current directory of this file
graph_visual_fil = curr_dir + "/" + "currencies_graph_visual.png"

pos=nx.circular_layout(g)
nx.draw_networkx(g,pos)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)

plt.savefig(graph_visual_fil)