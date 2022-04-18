import json
import mwparserfromhell
import re

with open('scrape/navboxes_osw.json') as infile:
    navs_osw = json.load(infile)

outlist = []

for i in range(len(navs_osw)):
    wikicode = mwparserfromhell.parse(navs_osw[i]['contents'])
    templates = wikicode.filter_templates()
    for j in range(len(templates)):
        if(templates[j].name.matches('navbox')):
            if(templates[j].has('title')):
                outlist.append(navs_osw[i]['title'] + '\t' + str(templates[j].get('title').value))

with open('navs/output.txt', 'w') as outfile:
    outfile.write(''.join(outlist))