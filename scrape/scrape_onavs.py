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
        "prop": "transcludedin",
        "titles": "Template:Navbox",
        "tiprop": "pageid",
        "tinamespace": 10,
        "tilimit": 50,
        "ticontinue": continueval,
        "format": "json"
    }
    print('current OSW progress:', len(biglist))
    response = requests.get(API_URL, params=params) #this next section is just to clean up the output
    pagelist = response.json()
    # print(pagelist)
    pageclean = pagelist['query']['pages']['1907']['transcludedin']


    listclean = [] #make an empty list
    for k in range(len(pageclean)):
        listclean.append(str(pageclean[k]['pageid'])) #and now fill that list with comma separated page ids

    listclean = "|".join(listclean) #Now we have a bunch of bar separated pageids

    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "format": "json", 
        "pageids": listclean,
    }

    response = requests.get(API_URL, params=params) #here we ask for all the info on those pageids
    revision = response.json()
    revision = revision['query']['pages'] #here's the info
    revlist = list(revision) #and here's the pageids to iterate by

    for j in range(len(revlist)): #for as many pages as I grabbed...
        page = revision[revlist[j]] #pull out that page
        tempdict = {
            'title': page['title'],
            'contents': page['revisions'][0]['*']
        }
        biglist.append(tempdict)
    
    if 'continue' in pagelist: #if we have a continue section
        continueval = pagelist['continue']['ticontinue'] #grab the continue and send it on back to the start
    else: #if no continue section,
        break #stop the while loop

with open('scrape/navboxes_osw.json', 'w') as outfile:
    json.dump(biglist, outfile)