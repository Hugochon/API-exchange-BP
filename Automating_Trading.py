import requests;
import json;

endpoint = "https://data.binance.com"

# Prints the list of all available cryptoes on
def get_all_available_crypto(): 
    response = requests.get(endpoint + "/api/v3/exchangeInfo")
    json_response = response.json()

    for s in json_response['symbols']:
        print(s['symbol'])
    
# Prints the bids or asks of a specific Pair (default being the first asks for BTCUSDT)
def get_bids_or_asks(direction = 'asks',symbol = "BTCUSDT"): 
    response = requests.get(endpoint + "/api/v3/depth?symbol=" + symbol + "&limit=1")
    json_response = response.json()
    print(json_response[direction])


# Prints the whole OrderBook of a specific Pair (default being BTCUSDT)
def get_orderbook(symbol = "BTCUSDT"): 
    response = requests.get(endpoint + "/api/v3/depth?symbol=" + symbol)
    json_response = response.json()
    print(json_response)

def candles(interval = "5", symbol = "BTCUSDT"): 
    response = requests.get(endpoint + "/api/v3/klines?symbol=" + symbol + "&interval=" + interval)
    json_response = response.json()
    print(json_response)

candles()