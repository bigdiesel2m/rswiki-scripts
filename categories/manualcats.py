import json
import mwparserfromhell
import re

# this section gets a big list of manual categories, either by parsing the page contents or loading a pre-existing list
regenerate = False
outjson = []
if regenerate:
    with open('scrape/contents_osw.json') as infile:
        data_osw = json.load(infile)
    for i in range(len(data_osw)):
        catregex = re.compile(r'\[\[Category:.*\]\]')
        mo = catregex.findall(data_osw[i]['contents'])
        for j in range(len(mo)):
            catclean = mo[j][11:-2]
            outjson.append(catclean)
    with open('categories/catlist.json', 'w') as outfile:
        json.dump(outjson, outfile)
else:
    with open('categories/catlist.json') as infile:
        outjson = json.load(infile)

# this section makes a big list of categories