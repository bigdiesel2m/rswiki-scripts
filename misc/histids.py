import json
import mwparserfromhell
import re

def cleanid(id):
    id = re.sub(r'[0-9]', '', id)
    id = re.sub(r'\,', '', id)
    id = id.strip(' \n')
    return(id)

def checkremoval(ver):
    if not (infobox.has('removal') or infobox.has('removal'+ver)):
        pageinfo['vers'].append(ver)
        pageinfo['ids'].append(id)
    

with open('scrape/contents_osw.json') as infile: #grab the >data<
    data_osw = json.load(infile)

outputlist = []
for i in range(len(data_osw)):
    if i%1000==0:
        print('current step:',i)
    page = data_osw[i]

    pageinfo = {
        'title': page['title'],
        'vers': [],
        'ids': [],
    }

    wikitext = mwparserfromhell.parse(page['contents'])
    infobox = wikitext.filter_templates(matches=lambda t: t.name.matches('Infobox NPC'))
    if infobox:
        infobox = infobox[0]
        if infobox.has('id'):
            id = cleanid(str(infobox.get('id').value))
            if id:
                checkremoval('')
        for i in range(20):
            if infobox.has('id'+str(i)):
                id = cleanid(str(infobox.get('id'+str(i)).value))
                if id:
                    checkremoval(str(i))
    if pageinfo['ids']:
        outputlist.append(pageinfo)


with open('misc/output.json', 'w') as outfile:
    json.dump(outputlist, outfile)

justdata = []

for i in range(len(outputlist)):
    values = list(outputlist[i].values())
    for j in range(len(values)):
        values[j] = str(values[j])
    values = '\t'.join(values)
    justdata.append(values)

justdata = '\n'.join(justdata)

with open('misc/output.txt', 'w') as outfile:
    outfile.write(justdata)
