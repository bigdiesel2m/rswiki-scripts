import json
import mwparserfromhell
import login
import os

# This func part takes a given id, then gets the corresponding options for that item from the cache
def idopts(idstr):
	filename = 'dump/item_defs/' + idstr + '.json'
	if not os.path.isfile(filename):
		return('Error', 'Error', 'None')
	with open(filename) as infile:
		data_cache = json.load(infile)
	alloptions = (data_cache['interfaceOptions'])
	alloptions = list(filter(lambda item: item is not None, alloptions))
	if 'Drop' in alloptions:
		cleanoptions = list(filter(lambda item: item != 'Drop', alloptions))
		dropoption = 'Drop'
	elif 'Destroy' in alloptions:
		cleanoptions = list(filter(lambda item: item != 'Destroy', alloptions))
		dropoption = 'Destroy'
	else:
		cleanoptions = alloptions
		dropoption = 'None'
	alloptions = optionjoin(alloptions)
	cleanoptions = optionjoin(cleanoptions)
	return(alloptions, cleanoptions, dropoption)

# this func takes a list of options and makes it a comma-separated string, unless it's empty
def optionjoin(optlist):
	if optlist == []:
		return('None')
	else:
		return(', '.join(optlist))

# this func compares a set of values to what's in a given infobox param
def infocheck(infobox, param, valstring):
	if (infobox.has(param) and valstring == str(infobox.get(param).value.strip())):
		return(True)
	elif (valstring == 'None' and not infobox.has(param)):
		return(True)
	else:
		return(False)

# this function compares the options from the cache to those from the infobox, then calls the edit functions to fix any simple ones
def simplefix(alloptions, cleanoptions, dropoption, infobox, page, wikitext):
	if dropoption == 'Drop':
		if (infocheck(infobox, 'destroy', 'Drop') and infocheck(infobox, 'options', cleanoptions)):
			droplist.append(page['title'])
			infoedit(alloptions, page, wikitext, 'Drop')
		else:
			otherlist.append(page['title'])
	elif dropoption == 'Destroy':
		if (infobox.has('destroy') and infocheck(infobox, 'options', cleanoptions)):
			destroylist.append(page['title'])
			infoedit(alloptions, page, wikitext, 'Destroy')
		else:
			otherlist.append(page['title'])
	else:
		otherlist.append(page['title'])

API_URL = "https://oldschool.runescape.wiki/api.php"
session, token = login.login(API_URL)

def edit(page, text, revid): #Cook's edit code
	data={
		'format': 'json',
		'action': 'edit',
		'assert': 'user',
		'text': str(text),
		'summary': "infobox options adjustments",
		'title': page,
		'baserevid': revid,
		'bot': 1,
		'token': token
	}
	session.post(API_URL, data=data)

# This func edits a given page by replacing the options in the options param with the cleanoptions, then deleting the no longer necessary destroy param
def infoedit(alloptions, page, wikitext, droptype):
	# this edits the infobox to remove the destroy param and add the full options list
	for infobox in wikitext.filter_templates(matches=lambda t: t.name.matches('Infobox Item')):
		if infobox.has('options'):
			infobox.add('options', alloptions)
		else:
			if infobox.has('wornoptions'):
				infobox.add('options', alloptions, before='wornoptions')
			elif infobox.has('wornoptions1'):
				infobox.add('options', alloptions, before='wornoptions1')
			elif infobox.has('destroy'):
				infobox.add('options', alloptions, before='destroy')
			elif infobox.has('destroy1'):
				infobox.add('options', alloptions, before='destroy1')
			elif infobox.has('examine'):
				infobox.add('options', alloptions, before='examine')
			elif infobox.has('examine1'):
				infobox.add('options', alloptions, before='examine1')
			else:
				break
		if droptype == 'Drop':
			infobox.remove('destroy')
	#edit(page['title'], wikitext, page['revid'])

with open('scrape/contents_osw.json') as infile:
	data_wiki = json.load(infile)

# set up some lists to fill with pagenames to count which ones are easy to handle
outputlist = []
multboxlist = []
itemlist = []
droplist = []
destroylist = []
versionlist = []
verdiflist = []
weirdidlist = []
otherlist = []

for i in range(len(data_wiki)):
#for i in range(1000):
	if i%1000==0:
		print('current step:',i)
	page = data_wiki[i]
	wikitext = mwparserfromhell.parse(page['contents'])
	infobox = wikitext.filter_templates(matches=lambda t: t.name.matches('Infobox Item'))
	if infobox:
		itemlist.append(page['title'])
		# This part filters out some odd cases I don't want to handle right now
		if len(infobox) > 1:
			multboxlist.append(page['title'])
			continue
		infobox = infobox[0]
		if infobox.has('version1'):
			# special handling for versioned infoboxes
			versionlist.append(page['title'])
			versioncount = 0
			while True:
				versioncount = versioncount + 1
				if not infobox.has('version' + str(versioncount + 1)):
					break
			# at this point we have the number of versions in the versioncount var
			# now we get the info for the first id
			if not infobox.has('id1') or not str(infobox.get('id1').value.strip()).isnumeric():
				weirdidlist.append(page['title'])
				continue
			alloptions, cleanoptions, dropoption = idopts(str(infobox.get('id1').value.strip()))

			idsokay = True
			for j in range(2,versioncount+1):
				if not infobox.has('id'+str(j)) or not str(infobox.get('id'+str(j)).value.strip()).isnumeric():
					weirdidlist.append(page['title'])
					idsokay = False
					break # break if some versions don't have regular ids
				veropts, _, _ = idopts(str(infobox.get('id'+str(j)).value.strip()))
				if not (veropts == alloptions):
					verdiflist.append(page['title'])
					idsokay = False
					break # break if some versions have different options
			if (idsokay): # at this point, we know that all ids in the infobox are regular and all have the same options
				simplefix(alloptions, cleanoptions, dropoption, infobox, page, wikitext)
			continue

		# back to normal infoboxes now
		if not infobox.has('id') or not str(infobox.get('id').value.strip()).isnumeric():
			weirdidlist.append(page['title'])
			continue
		
		[alloptions, cleanoptions, dropoption] = idopts(str(infobox.get('id').value.strip()))

		simplefix(alloptions, cleanoptions, dropoption, infobox, page, wikitext)

# Everything past here is just for ouput checking and counting stuff
print([len(itemlist), len(multboxlist), len(versionlist), len(verdiflist), len(weirdidlist), len(droplist), len(destroylist), len(otherlist)])
outputlist = [itemlist, multboxlist, versionlist, verdiflist, weirdidlist, droplist, destroylist, otherlist]

with open('options/output.json', 'w') as outfile:
	json.dump(outputlist, outfile)

outtxt = ['\t'.join(multboxlist), '\t'.join(versionlist), '\t'.join(verdiflist), '\t'.join(weirdidlist), '\t'.join(droplist), '\t'.join(destroylist), '\t'.join(otherlist)]
outtxt = '\n'.join(outtxt)

with open('options/output.txt', 'w') as outfile:
	outfile.write(outtxt)