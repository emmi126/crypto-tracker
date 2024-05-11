import requests
from bs4 import BeautifulSoup
import json
import pandas

URL = 'https://coinmarketcap.com/'
req = requests.get(URL)
soup = BeautifulSoup(req.content, "html.parser")
results = soup.find('script', id='__NEXT_DATA__', type='application/json')

# Create dictionary of slugs and IDs
coins = {}
content = json.loads(results.contents[0])
data = content['props']['initialState']['cryptocurrency']['listingLatest']['data']
for i in data:
    coins[str(i['id'])] = i['slug']

# Obtain cryptocurrency data for each coin
for i in coins:
    URL_spec = "f'https://coinmarketcap.com/currencies/{coins[i]}/historical-data/?start=20220101&end=20230101"
    req = requests.get(URL_spec)
    soup = BeautifulSoup(req.content, "html.parser")
    results = soup.find('script', id='__NEXT_DATA__', type='application/json')
    historical_content = json.loads(results.contents[0])
    quotes = historical_content['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]['quotes']
    record = historical_content['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]

# Store data in pandas
cap = []
vol = []
time = []
name = []
symbol = []
slug = []

for i in quotes:
    cap.append(i['quote']['USD']['market_cap'])
    vol.append(i['quote']['USD']['volume'])
    time.append(i['quote']['USD']['timestamp'])
    name.append(record['name'])
    symbol.append(record['symbol'])
    slug.append(coins[i])

dframe = pandas.DataFrame(columns = ['marketcap', 'volume', 'timestamp', 'name', 'symbol', 'slug'])
dframe['market_cap'] = cap
dframe['volume'] = vol
dframe['timestamp'] = time
dframe['name'] = name
dframe['symbol'] = symbol
dframe['slug'] = slug

# Save to a CSV file
dframe.to_csv('cryptocurrency.csv', index=False)
