import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST

# authentication and connection details
api_key = 'PKAZDKWPN9XTS0TPPXIF'
api_secret = 'dtGGSlvXtB08mKCRdzAQol77cvHoOlvjyxEzg0DO'
base_url = 'https://paper-api.alpaca.markets'

# instantiate REST API
api = REST(api_key, api_secret, base_url)

# obtain account information
account = api.get_account()
print(account)