import csv
from itertools import permutations
from datetime import datetime
import os

# Simulate a list of currencies
currencies = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']
currency_map = {currency: f"id_{i}" for i, currency in enumerate(currencies)}

# Simulate the API data for exchange rates between the currencies
# In a real-world scenario, this would be fetched from an API like CoinGecko
api_data = {
    'id_0': {'ETH': 0.05, 'XRP': 200, 'LTC': 10, 'BCH': 0.5},  # BTC exchange rates to other currencies
    'id_1': {'BTC': 20, 'XRP': 4000, 'LTC': 200, 'BCH': 10},  # ETH exchange rates to other currencies
    'id_2': {'BTC': 0.005, 'ETH': 0.00025, 'LTC': 0.05, 'BCH': 0.0025},  # XRP exchange rates to other currencies
    'id_3': {'BTC': 0.1, 'ETH': 5, 'XRP': 0.02, 'BCH': 0.25},  # LTC exchange rates to other currencies
    'id_4': {'BTC': 2, 'ETH': 50, 'XRP': 0.5, 'LTC': 4}  # BCH exchange rates to other currencies
}

curr_dir = os.path.dirname(__file__)
file_path = os.path.join(curr_dir, "crypto_ids.txt")
data_folder = os.path.join(curr_dir, "data")

# Get the current timestamp
timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M")

# Create the filename
filename = os.path.join(data_folder, f"currency_pair_{timestamp}.txt")

print(filename)

# Open the file for writing
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["currency_from", "currency_to", "exchange_rate"])  # Header

    # Add data while building the graph (simulated here with mock data)
    for c1, c2 in permutations(currencies, 2):
        if c1 != c2 and c2 in api_data[currency_map[c1]]:
            rate = api_data[currency_map[c1]][c2]

            # Write to CSV file
            writer.writerow([c1, c2, rate])

print(f"Currency pair data has been saved to {filename}")
