# This is the url that I used  to get the exchange rates of each crypto currency
# "https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={vs_currencies}"

# This is the base url that I used to place paper orders
# "https://paper-api.alpaca.markets"

# importing libraries
import os
import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

# libraries needed for paper trading with Alpaca
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST

# my api keys with Alpaca
api_key = 'PKAZDKWPN9XTS0TPPXIF'
api_secret = 'dtGGSlvXtB08mKCRdzAQol77cvHoOlvjyxEzg0DO'

# function to calculate the weight of a path by multiplying the weights together
def calculate_path_weight(g, path   ):
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

                print(f'\033[1mPaths from {start} to {end}----------------------------------------------\033[0m')

                # calculate the weight of forward paths
                for forward_path in forward_paths:
                    forward_weight = calculate_path_weight(g,forward_path)

                    # calculate the weight of reverse paths
                    for reverse_path in reverse_paths:
                        reverse_weight = calculate_path_weight(g,reverse_path)

                        # multiply the weights to get the arbitrage factor
                        factor = forward_weight * reverse_weight
                        # print all the paths and their factors
                        print(forward_path)
                        print(reverse_path)
                        print(factor)

                        

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
                                    

def alpaca_get_account():
    r = requests.get(account_url, headers = header)

    return json.loads(r.content)

def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "class": 'crypto',
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(orders_url,json=data, headers = header)

    return json.loads(r.content)

# file the cyrpto currencies are listed in
curr_dir = os.path.dirname(__file__)
file_path = os.path.join(curr_dir, "crypto_ids.txt")

# urls needs for 
base_url = "https://paper-api.alpaca.markets"
account_url = "{}/v2/account". format(base_url)
orders_url = "{}/v2/orders". format(base_url)
header = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}

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
        data = req.json()
        
        # add the node info from the API
        for c1, c2 in permutations(currencies, 2):
            if c1 != c2 and c2 in data[currency_map[c1]]:
                rate = data[currency_map[c1]][c2]
                g.add_edge(c1, c2, weight=rate)

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

# in case there is an error for finding paths    
except Exception as e:
    print(f"Error during path finding: {e}")

#forward_path, reverse_path, factor  = find_paths(g)
#print(forward_path, reverse_path, factor)

# printing a graph of the currency exchange rates
curr_dir = os.path.dirname(__file__) # get the current directory of this file
graph_visual_fil = curr_dir + "/" + "currencies_graph_visual.png"

pos=nx.circular_layout(g)
nx.draw_networkx(g,pos)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)

plt.savefig(graph_visual_fil)