import requests;
import json;
import sqlite3;
import websocket;

endpoint = "https://data.binance.com"

# Database related functions
sqliteConnection = sqlite3.connect('mydb.db')
cursor = sqliteConnection.cursor()

cursor.execute("DROP TABLE IF EXISTS candlestable")
cursor.execute("DROP TABLE IF EXISTS tradestable")

query_candlestable = """CREATE TABLE candlestable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pair TEXT, 
        date INT,
        high REAL,
        low REAL,
        open REAL,
        close REAL,
        volume REAL
    );"""

query_tradestable ='''CREATE TABLE tradestable(
   id INTEGER PRIMARY KEY AUTOINCREMENT, 
   uuid TEXT, 
   traded_crypto TEXT,
   price REAL,
   created_at INT, 
   side TEXT
)'''

cursor.execute(query_candlestable)
sqliteConnection.commit()
cursor.execute(query_tradestable)
sqliteConnection.commit()

query_insert_candlesdata = """
INSERT INTO candlestable (pair, date, high, low, open, close, volume)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""
query_insert_tradesdata = """
INSERT INTO tradestable (uuid, traded_crypto,price,created_at, side)
VALUES (?, ?, ?, ?, ?)
"""

# Prints the list of all available crypto pairs on Binance
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

# Prints the candles of a specific Pair (default being BTCUSDT) and interval (default being 5 mintues) and limit (default being 500)
def candles(interval = "5m", symbol = "BTCUSDT", limit = 500): 
    response = requests.get(endpoint + "/api/v3/klines?symbol=" + symbol + "&interval=" + interval + "&limit=" + str(limit))
    json_response = response.json()
    data = []
    for i in range(len(json_response)):
        data.append((symbol,json_response[i][0],json_response[i][2],json_response[i][3],json_response[i][1],json_response[i][4],json_response[i][5]))
    cursor.executemany(query_insert_candlesdata, data)
    sqliteConnection.commit()

# Prints the trades of a specific Pair (default being BTCUSDT) and limit (default being 500)
def trades(symbol = "BTCUSDT",limit = 500): 
    response = requests.get(endpoint + "/api/v3/trades?symbol=" + symbol + "&limit=" + str(limit))
    json_response = response.json()
    data = []
    for i in range(len(json_response)):
        data.append((json_response[i]['id'],symbol,json_response[i]['price'],json_response[i]['time'],json_response[i]['isBuyerMaker']))
    cursor.executemany(query_insert_tradesdata, data)
    sqliteConnection.commit()

def print_menu():
  print("1. Get all pairs listed on binance")
  print("2. Get the bid or ask on a pair")
  print("3. Get the orderbook on a pair")
  print("4. Get candles on a pair")
  print("5. Get trades on a pair")
  print("6. Quit")

def menu():
  while True:
    print_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
      print("\nYou selected option 1")
      get_all_available_crypto()

    elif choice == "2":
      print("\nYou selected option 2")
      # Add as parameters the direction and the pair (default being asks and BTCUSDT)
      get_bids_or_asks()

    elif choice == "3":
      print("\nYou selected option 3")
      # Add as a parameter the pair (default being BTCUSDT)
      get_orderbook()
   
    elif choice == "4":
      print("\nYou selected option 4")
      # Add as parameters the interval, the pair and the limit (default being 5m, BTCUSDT and 500)
      candles()
      query_select_price = "SELECT * FROM candlestable"
      cursor.execute(query_select_price)
      results = cursor.fetchall()

      for row in results:
        print(row)

    elif choice == "5":
      print("\nYou selected option 5")
      # Add as parameters the pair and the limit (default being BTCUSDT and 500)
      trades()
      query_select_price = "SELECT * FROM tradestable"
      cursor.execute(query_select_price)
      results = cursor.fetchall()

      for row in results:
        print(row)

    elif choice == "6":
      break
    else:
      print("\nInvalid choice. Please try again.\n")
    print("")

menu()
sqliteConnection.close()