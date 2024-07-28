import requests
import json

API_URL = "https://api.weirdgloop.org/exchange/history/osrs/last90d" #base api url

with open('pricecompare/mapping.json', 'r') as infile:
    mapping = json.load(infile)

outlist = []
itemcount = 0
for item in mapping:
    itemcount = itemcount + 1
    if (itemcount % 25) == 0:
        print("Progress: " + str(itemcount))

    id = str(item['id'])

    params = {
        "id": id, #ask for a list of all categorires
    }
    responsejson = requests.get(API_URL, params=params).json()
    outlist.append(responsejson)

with open('pricecompare/90dprices.json', 'w') as outfile:
    json.dump(outlist, outfile) 