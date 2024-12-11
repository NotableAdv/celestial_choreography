import requests
import json

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST

api_key = 'PKAZDKWPN9XTS0TPPXIF'
api_secret = 'dtGGSlvXtB08mKCRdzAQol77cvHoOlvjyxEzg0DO'

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account". format(BASE_URL)
ORDERS_URL = "{}/v2/orders". format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}

def get_account():
    r = requests.get(ACCOUNT_URL, headers = HEADERS)

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
    r = requests.post(ORDERS_URL,json=data, headers = HEADERS)

    return json.loads(r.content)

response = create_order('ETH/USD', 1, 'buy', 'market', 'gtc')

print(response)