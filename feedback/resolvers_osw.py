import requests
import json
from collections import Counter

# Disclaimer, this is probably a really dumb/inefficient way to count up feedback resolvers, but I don't know a smarter way to do it and the sample size isn't so large that it's a problem to do a few thousand api calls, I hope

API_URL = "https://oldschool.runescape.wiki/api.php"

with open('feedback/resolved_pages_osw.json') as infile:
	resolvelist = json.load(infile)

delstr = '<td class="diff-deletedline diff-side-deleted"><div>|resolved=<del class="diffchange diffchange-inline">no</del></div></td>'
addstr = '<td class="diff-addedline diff-side-added"><div>|resolved=<ins class="diffchange diffchange-inline">yes</ins></div></td>'

userlist = []
for page in resolvelist:
	if len(userlist) % 10 == 0:
		print(len(userlist))
	# GET REVISIONS
	revlist = []
	params = {
		"action": "query",
		"prop": "revisions",
		"rvprop": "ids",
		"rvstart": "2024-06-20T12:00:00Z",
		"rvend": "now",
		"rvdir": "newer",
		"format": "json", 
		"pageids": page['pageid'],
	}
	response = requests.get(API_URL, params=params) #this next section is just to clean up the output
	responsejson = response.json()
	revlist = responsejson["query"]["pages"][str(page['pageid'])]['revisions']
	
	for rev in revlist:
		if rev["parentid"] != 0: # We can skip any that are page creations
			params = {
				"action": "compare",
				"fromrev": rev["parentid"],
				"torev": rev["revid"],
				"prop": "diff|user",
				"format": "json", 
			}
			response = requests.get(API_URL, params=params) #this next section is just to clean up the output
			responsejson = response.json()
			text = responsejson["compare"]["*"]
			if delstr in text and addstr in text:
				userlist.append(responsejson["compare"]["touser"])

counted = Counter(userlist)

outlist = []
for user in counted:
	outlist.append(user + "\t" + str(counted[user]))

with open('feedback/resolvercount_osw.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))