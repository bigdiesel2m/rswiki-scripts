import requests
import json

API_URL = "https://runescape.wiki/api.php" #we don't need this to change, so might as well set it here

biglist = []
continueval = ""
while True: #run until we break
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": "Category:Pages with resolved feedback",
        "cmlimit": 50,
        "cmprop": "ids",
        "cmcontinue": continueval #starting here
    }
    print('current RSW progress:', len(biglist))
    response = requests.get(API_URL, params=params) #this next section is just to clean up the output
    catlist = response.json()
    biglist = biglist + catlist['query']['categorymembers']
    
    if 'continue' in catlist: #if we have a continue section
        continueval = catlist['continue']['cmcontinue'] #grab the continue and send it on back to the start
    else: #if no continue section,
        break #stop the while loop

with open('feedback/resolved_pages_rsw.json', 'w') as outfile:
    json.dump(biglist, outfile)