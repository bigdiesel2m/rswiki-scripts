import json
import mwparserfromhell

def optionjoin(optlist):
	if optlist == []:
		return('None')
	else:
		return(', '.join(optlist))

def infocheck(param, valstring):
	if (infobox.has(param) and valstring == str(infobox.get(param).value.strip())):
		return(True)
	elif (valstring == 'None' and not infobox.has(param)):
		return(True)
	else:
		return(False)



with open('scrape/contents_osw.json') as infile: #grab the >data<
	data_wiki = json.load(infile)
	

outputlist = []
multboxlist = []
itemlist = []
droplist = []
destroylist = []
versionlist = []
weirdidlist = []
otherlist = []
for i in range(len(data_wiki)):
#for i in range(500):
	if i%1000==0:
		print('current step:',i)
	page = data_wiki[i]
	wikitext = mwparserfromhell.parse(page['contents'])
	infobox = wikitext.filter_templates(matches=lambda t: t.name.matches('Infobox Item'))
	if infobox:
		if len(infobox) > 1:
			multboxlist.append(page['title'])
		else:
			infobox = infobox[0]
			itemlist.append(page['title'])
			if infobox.has('version1'):
				versionlist.append(page['title'])
			else:
				if not infobox.has('id'):
					weirdidlist.append(page['title'])
				else:
					if not str(infobox.get('id').value.strip()).isnumeric():
						weirdidlist.append(page['title'])
					else: #okay now that we have all the weird cases hopefully filtered out
						# This next part takes the id from the infobox, then gets the info about the matching item
						idstr = str(infobox.get('id').value.strip())
						with open('dump/item_defs/' + idstr + '.json') as infile:
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
						# Now that we have all the options, the non-drop options, and the drop options, let's compare with the infobox params
						if dropoption == 'Drop':
							if (infocheck('destroy', 'Drop') and infocheck('options', cleanoptions)):
								droplist.append(page['title'])
							else:
								otherlist.append(page['title'])
						elif dropoption == 'Destroy':
							if (infobox.has('destroy') and infocheck('options', cleanoptions)):
								destroylist.append(page['title'])
							else:
								otherlist.append(page['title'])
						else:
							otherlist.append(page['title'])


print([len(itemlist), len(multboxlist), len(versionlist), len(weirdidlist), len(droplist), len(destroylist), len(otherlist)])
outputlist = [itemlist, multboxlist, versionlist, weirdidlist, droplist, destroylist, otherlist]

with open('options/output.json', 'w') as outfile:
	json.dump(outputlist, outfile)

for element in outputlist:
	element = ','.join(element)

outtxt = ['\t'.join(multboxlist), '\t'.join(versionlist), '\t'.join(weirdidlist), '\t'.join(droplist), '\t'.join(destroylist), '\t'.join(otherlist)]
outtxt = '\n'.join(outtxt)

with open('options/output.txt', 'w') as outfile:
    outfile.write(outtxt)