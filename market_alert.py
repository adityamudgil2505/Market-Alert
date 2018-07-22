import os
import json
import requests
import time
from datetime import datetime

convert = input('Enter the currency code: ')
convert = convert.upper()

listing_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
end_url = '?structure=array&convert='+convert
ticking_url_pair = {}
request = requests.get(listing_url)
result = request.json()
data = result['data']

for currency in data:
    symbol = currency['symbol']
    id = currency['id']
    ticking_url_pair[symbol] = id

print('\nAlert Tracking')
already_hit_symbol = []

while True:
    with open('alert.txt') as inp:
        for line in inp:
            asset,amount = line.split()
            asset = asset.upper()
            ticking_url = 'https://api.coinmarketcap.com/v2/ticker/'+str(ticking_url_pair[asset])+end_url
            request = requests.get(ticking_url)
            result = request.json()
            data = result['data'][0]

            name = data['name']
            symbol = data['symbol']
            price = data['quotes'][convert]['price']
            last_updated = data['last_updated']
            if float(price) >= float(amount) and asset not in already_hit_symbol:
                os.system('say '+ name + 'hits' + amount)
                last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %H:%m%p')
                print('{} ({}) hits {} on {}'.format(name,symbol,amount,last_updated_string))
                already_hit_symbol.append(symbol)
    print('...')
    time.sleep(300)
