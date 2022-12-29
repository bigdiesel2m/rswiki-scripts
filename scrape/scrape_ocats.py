import sys
import requests
import json
import math
import mwparserfromhell

API_URL = "https://oldschool.runescape.wiki/api.php" #we don't need this to change, so might as well set it here

biglist = []
continueval = ""
while True: #run until we break
    params = {
        "action": "query",
        "format": "json",
        "list": "allcategories", #ask for a list of all categorires
        "aclimit": 50, #max of 500, testing at less right now
        "acprop": "size",
        "accontinue": continueval #starting here
    }
    print('current OSW progress:', len(biglist))
    response = requests.get(API_URL, params=params) #this next section is just to clean up the output
    catlist = response.json()
    biglist = biglist + catlist['query']['allcategories']
    
    if 'continue' in catlist: #if we have a continue section
        continueval = catlist['continue']['accontinue'] #grab the continue and send it on back to the start
    else: #if no continue section,
        break #stop the while loop

with open('scrape/categories_osw.json', 'w') as outfile:
    json.dump(biglist, outfile)