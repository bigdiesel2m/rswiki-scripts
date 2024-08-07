import requests
import json

API_URL = "https://oldschool.runescape.wiki/api.php" #we don't need this to change, so might as well set it here

biglist = []
continueval = ""
while True: #run until we break
	params = {
		"action": "query",
		"format": "json",
		"list": "categorymembers",
		"cmtitle": "Category:12 Days of Dragon Sleigher",
		"cmtype": "file",
		"cmlimit": 50, #max of 500, testing at less right now
		"cmcontinue": continueval #starting here
	}
	print('current OSW progress:', len(biglist))
	response = requests.get(API_URL, params=params) #this next section is just to clean up the output
	pagelist = response.json()
	pageclean = pagelist['query']['categorymembers']

	listclean = [] #make an empty list
	for k in range(len(pageclean)):
		listclean.append(str(pageclean[k]['pageid'])) #and now fill that list with comma separated page ids

	listclean = "|".join(listclean) #Now we have a bunch of bar separated pageids
	
	params = {
		"action": "query",
		"prop": "imageinfo",
		"iiprop": "url",
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
			'url': page['imageinfo'][0]['url']
		}
		biglist.append(tempdict)
	
	if 'continue' in pagelist: #if we have a continue section
		continueval = pagelist['continue']['apcontinue'] #grab the continue and send it on back to the start
	else: #if no continue section,
		break #stop the while loop

with open('scrape/dii_osw.json', 'w') as outfile:
	json.dump(biglist, outfile)