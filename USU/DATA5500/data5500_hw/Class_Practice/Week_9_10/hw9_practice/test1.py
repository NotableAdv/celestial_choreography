import os
import requests
import json
from itertools import permutations
import networkx as nx

# File containing the list
curr_dir = os.path.dirname(__file__)
file_path = os.path.join(curr_dir, "crypto_ids.txt")

# Read currencies from file
currencies = []
currency_map = {}
with open(file_path, "r") as file:
    for line in file:
        name, symbol = line.strip().split(",")
        currencies.append(symbol)
        currency_map[symbol] = name

# Initialize graph
g = nx.DiGraph()
edges = []

# Base API URL
base_url_template = 'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={vs_currencies}'

# Generate all permutations of currency pairs
for c1, c2 in permutations(currencies, 2):  # c1 to c2
    # Build the API URL for the pair
    ids = f"{currency_map[c1]},{currency_map[c2]}"
    vs_currencies = f"{c1},{c2}"
    url = base_url_template.format(ids=ids, vs_currencies=vs_currencies)
    
    try:
        # Make the API request
        req = requests.get(url)
        req.raise_for_status()  # Raise error for HTTP issues
        data = req.json()

        # Extract exchange rate
        if c2 in data[currency_map[c1]]:
            rate = data[currency_map[c1]][c2]
            edges.append((c1, c2, rate))  # Add directed edge with weight
    
        else:
            print(f"Rate not found for {c1} to {c2}")
    except Exception as e:
        print(f"Error fetching data for {c1} to {c2}: {e}")

# Add edges to the graph
g.add_weighted_edges_from(edges)