import json
import mwparserfromhell
import re

# this section gets a big list of manual categories, either by parsing the page contents or loading a pre-existing list
regenerate = True
outjson = []
if regenerate:
    with open('scrape/contents_osw.json') as infile:
        data_osw = json.load(infile)
    for i in range(len(data_osw)):
        catregex = re.compile(r'\[\[Category:.*?\]\]')
        mo = catregex.findall(data_osw[i]['contents'])
        for j in range(len(mo)):
            catclean = mo[j][11:-2]
            outjson.append(catclean)
    with open('categories/output.json', 'w') as outfile:
        json.dump(outjson, outfile)
else:
    with open('categories/output.json') as infile:
        outjson = json.load(infile)

# this section takes the list of categoires and compares that to the manual categories, then outputs the data into a txt file
with open('scrape/categories_osw.json') as infile:
    cats_osw = json.load(infile)

outlist = []
for i in range(len(cats_osw)):
    linkthing = 'https://oldschool.runescape.wiki/?search=insource%3A%2F\[\[Category\%3A' + cats_osw[i]['*'].replace(' ', '+') + '\]\]%2F&title=Special%3ASearch&profile=default&fulltext=1'
    outstr = cats_osw[i]['*'] + '\t' + str(cats_osw[i]['size']) + '\t' + str(cats_osw[i]['pages']) + '\t' + str(outjson.count(cats_osw[i]['*'])) + '\t' + linkthing
    outlist.append(outstr)

with open('categories/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))


# this section separates out oddball cases that might not be picked up by the other filters
exceptionlist = []
for i in range(len(outjson)):
    if '|' in outjson[i]:
        exceptionlist.append(outjson[i])

with open('categories/exceptions.txt', 'w') as outfile:
    outfile.write('\n'.join(exceptionlist))

print('Categories: ' + str(len(cats_osw)))
print('Manual Categorizations: ' + str(len(outjson)))
print('Exceptions: ' + str(len(exceptionlist)))
