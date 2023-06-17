import json
import mwparserfromhell

def histcheck(pagename, version, idparam):
	if 'hist' in idparam:
		idparam = idparam.replace('hist','')
		if idparam != '':
			idlist.append(str(idparam))
		outputlist.append(pagename + '\t' + str(version) + '\t' + str(idparam))
	return

with open('scrape/contents_osw.json') as infile:
	data_wiki = json.load(infile)

# set up some lists to fill with pagenames to count which ones are easy to handle
outputlist = []
idlist = []
for i in range(len(data_wiki)):
#for i in range(1000):
	if i%1000==0:
		print('current step:',i)
	page = data_wiki[i]
	wikitext = mwparserfromhell.parse(page['contents'])
	infobox = wikitext.filter_templates(matches=lambda t: t.name.matches('Infobox Item'))
	if infobox:
		infobox = infobox[0]
		if infobox.has('version1'):
			versioncount = 0
			while True:
				versioncount = versioncount + 1
				if not infobox.has('version' + str(versioncount + 1)):
					break
			for j in range(1,versioncount+1):
				idparam = ''
				if infobox.has('id'+str(j)):
					idparam = infobox.get('id'+str(j)).value.strip()
				elif infobox.has('id'):
					idparam = infobox.get('id').value.strip()
				else:
					idparam = ''
				histcheck(page['title'], j, idparam)
		else:
			idparam = ''
			if infobox.has('id'):
				idparam = infobox.get('id').value.strip()
			else:
				idparam = ''
			histcheck(page['title'], 0, idparam)

outtxt = '\n'.join(outputlist)
idtxt = ','.join(idlist)

with open('options/output.txt', 'w') as outfile:
	outfile.write(outtxt)

with open('options/idlist.txt', 'w') as outfile:
	outfile.write(idtxt)