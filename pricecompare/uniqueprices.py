import requests
import json

API_URL = "https://api.weirdgloop.org/exchange/history/osrs/last90d" #base api url

with open('pricecompare/90dprices.json', 'r') as infile:
    prices = json.load(infile)

with open('pricecompare/mapping.json', 'r') as infile:
    mapping = json.load(infile)

outlist = []
itemcount = 0
for item in prices:
    id = list(item.keys())[0]

    pricelist = []
    volsum = 0
    pricesum = 0
    if type(item[id]) is list:
        for time in item[id]:
            price = time['price']
            if type(time['volume']) is int:
                volsum = volsum + time['volume']
            if type(time['price']) is int:
                pricesum = pricesum + time['price']
            if price not in pricelist:
                pricelist.append(time['price'])

        avgvol = volsum/len(item[id])
        avgprice = pricesum/len(item[id])

        # if avgvol > 100 and avgprice > 100:
        if avgvol > 1000 and len(pricelist) < 30 and avgprice > 10:
            name = ''
            for map in mapping:
                if map['id'] == int(id):
                    name = map['name']
            shortlist = [name, str(len(pricelist)), str(len(item[id])), str(avgvol), str(avgprice)]
            outlist.append("\t".join(shortlist))

with open('pricecompare/uniqueprices.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))