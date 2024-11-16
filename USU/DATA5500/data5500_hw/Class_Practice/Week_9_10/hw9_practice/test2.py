import os
import requests
import json
import networkx as nx
import matplotlib.pyplot as plt

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

# Batch size for currencies
batch_size = 50  # Adjust based on API limits

# Split currencies into batches
currency_batches = [currencies[i:i + batch_size] for i in range(0, len(currencies), batch_size)]

# Fetch exchange rates in batches
for batch in currency_batches:
    ids = ','.join([currency_map[sym] for sym in batch])
    vs_currencies = ','.join(currencies)  # Compare against all currencies
    url = base_url_template.format(ids=ids, vs_currencies=vs_currencies)
    
    try:
        # Make the API request
        req = requests.get(url)
        req.raise_for_status()  # Raise error for HTTP issues
        data = req.json()
        
        # Process the results
        for c1 in batch:
            for c2 in currencies:
                if c2 in data[currency_map[c1]]:
                    rate = data[currency_map[c1]][c2]
                    edges.append((c1, c2, rate))  # Add directed edge with weight
                else:
                    print(f"Rate not found for {c1} to {c2}")
    except Exception as e:
        print(f"Error fetching data for batch {batch}: {e}")

# Add edges to the graph
g.add_weighted_edges_from(edges)


curr_dir = os.path.dirname(__file__) # get the current directory of this file
graph_visual_fil = curr_dir + "/" + "test2_graph_visual.png"

pos=nx.circular_layout(g) # pos = nx.nx_agraph.graphviz_layout(G)
nx.draw_networkx(g,pos)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)

plt.savefig(graph_visual_fil)