import json
import mwparserfromhell
import re

regenerate = True

navlist = []
if regenerate:
    with open('scrape/navboxes_rsw.json') as infile:
        navs_osw = json.load(infile)
    for i in range(len(navs_osw)):
        wikicode = mwparserfromhell.parse(navs_osw[i]['contents'])
        templates = wikicode.filter_templates()
        for j in range(len(templates)):
            if(templates[j].name.matches('navbox')):
                if(templates[j].has('title')):
                    navlist.append(navs_osw[i]['title'])
            if(templates[j].name.matches('Quest navbox')):
                if(templates[j].has('title') or templates[j].has('name')):
                    navlist.append(navs_osw[i]['title'])
            if(templates[j].name.matches('Lore navbox')):
                if(templates[j].has('title') or templates[j].has('name')):
                    navlist.append(navs_osw[i]['title'])
    with open('navs/output.json', 'w') as outfile:
        json.dump(navlist, outfile)
else:
    with open('navs/output.json') as infile:
        navlist = json.load(infile)


with open('scrape/contents_rsw.json') as infile:
    list_osw = json.load(infile)

outlist = []
for i in range(len(list_osw)):
    if (i % 100 == 0):
        print(str(i) + ' / ' + str(len(list_osw)))
    count = 0
    wikicode = mwparserfromhell.parse(list_osw[i]['contents'])
    templates = wikicode.filter_templates()
    for j in range(len(templates)):
        propname = 'Template:' + templates[j].name[0].upper() + templates[j].name[1:]
        if(propname in navlist):
            count += 1
    outlist.append(list_osw[i]['title'] + '\t' + str(count))

with open('navs/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))