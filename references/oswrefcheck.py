# Script for scraping and then comparing references on OSW

import json
import mwparserfromhell
from collections import defaultdict


reftemplist = ["PlainCiteDevBlog","CiteDevBlog","PlainCiteForum","CiteForum","PlainCiteGeneral","CiteGeneral","PlainCiteGodLetter","CiteGodLetter","CiteLore","PlainCiteNews","CiteNews","PlainCiteNPC","CiteNPC","PlainCiteSupport","PlainCitePoll","CitePoll","PlainCitePostbag","CitePostbag","PlainCitePub","CitePub","PlainCiteReddit","CiteReddit","CiteText","PlainCiteTwitter","CiteTwitter","PlainCiteVideo","CiteVideo","PlainCiteDevBlog","CiteDevBlog","CiteDevDiary","PlainCiteDevDiary","PlainCiteDiscord","CiteDiscord","PlainCiteForum","CiteForum","PlainCiteGeneral","CiteGeneral","PlainCiteGodLetter","CiteGodLetter","PlainCiteLore","CiteLore","PlainCiteNews","CiteNews","PlainCiteNPC","CiteNPC","PlainCitePoll","CitePoll","PlainCitePostbag","CitePostbag","PlainCitePub","CitePub","PlainCiteReddit","CiteReddit","PlainCiteSupport","CiteSupport","PlainCiteText","CiteText","PlainCiteTwitter","CiteTwitter","PlainCiteVid"]

reflist = []

regenerate = False
if regenerate:
    with open('scrape/contents_osw.json') as infile:
        contents_osw = json.load(infile)
    for i in range(len(contents_osw)): # for each page
        if (i % 100 == 0): print(str(i))
        wikicode = mwparserfromhell.parse(contents_osw[i]['contents'])
        templates = wikicode.filter_templates() # get a list of templates on the page
        for j in range(len(templates)): # for each template
            if(templates[j].name.matches(reftemplist)): # find the ones that match the list of cite templates
                refdict = { # create a small dict to hold the info
                    "page" : contents_osw[i]['title'],
                    "template" : str(templates[j].name),
				}
                if(templates[j].has('url')): # condiditionally fill in the url and archive url params
                    refdict["url"] = (str(templates[j].get('url')))
                if(templates[j].has('archiveurl')):
                    refdict["archiveurl"] = (str(templates[j].get('archiveurl')))
                reflist.append(refdict)
    with open('references/references.json', 'w') as outfile: # dump it to output
        json.dump(reflist, outfile)
else:
    with open('references/references.json') as infile:
        reflist = json.load(infile)

archiveset = set()
for i in range(len(reflist)):
    if 'url' in reflist[i] and 'archiveurl' in reflist[i]:
        archiveset.add((reflist[i]['url'], reflist[i]['archiveurl']))

outlist = []

dA = defaultdict(set)
dB = defaultdict(set)

for a, b in archiveset:
    dA[a].add(b)
    dB[b].add(a)

for k, v in dA.items():
    if len(v) > 1:
        outlist.append(str(k) + '\t' + str(v))

outlist.append('')

for k, v in dB.items():
    if len(v) > 1:
        outlist.append(str(k) + '\t' + str(v))
        
with open('references/ouput.json', 'w') as outfile: # dump it to output
	json.dump(outlist, outfile)
    
with open('references/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))