import json
import login

API_URL = "https://oldschool.runescape.wiki/api.php" #we don't need this to change, so might as well set it here

session, token = login.login(API_URL)

biglist = []
continueval = ""
while True: #run until we break
    params = {
        "action": "query",
        "format": "json",
        "generator": "allpages", #ask for a list of all pages
        "gapnamespace": "0",
        "gapfilterredir": "nonredirects", #without redirects
        "gaplimit": 500,
        "gapcontinue": continueval, #starting here
        "prop": "revisions",
        "rvprop": "content|ids",
    }
    print('current OSW progress:', len(biglist))
    response = session.get(API_URL, params=params) #this next section is just to clean up the output
    responsejson = response.json()
    pages = responsejson['query']['pages']

    for page in pages: #for as many pages as I grabbed...
        tempdict = {
            'title': pages[page]['title'],
            'contents': pages[page]['revisions'][0]['*'],
            'revid': pages[page]['revisions'][0]['revid']
        }
        biglist.append(tempdict)
    
    if 'continue' in responsejson: #if we have a continue section
        continueval = responsejson['continue']['gapcontinue'] #grab the continue and send it on back to the start
    else: #if no continue section,
        break #stop the while loop

with open('scrape/contents_osw.json', 'w') as outfile:
    json.dump(biglist, outfile)