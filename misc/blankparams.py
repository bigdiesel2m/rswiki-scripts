import json
import mwparserfromhell

with open('scrape/contents_osw.json') as infile: #grab the >data<
    data_osw = json.load(infile)

outputlist = []
for i in range(len(data_osw)):
    if i%1000==0:
        print('current step:',i)
    page = data_osw[i]
    wikitext = mwparserfromhell.parse(page['contents'])
    otheruses = wikitext.filter_templates(matches=lambda t: t.name.matches('Otheruses'))
    
    if otheruses:
        pageinfo = {
            'title': page['title'],
            'vers': [],
        }
        for j in range(len(otheruses)):
            template = otheruses[j]
            if template.has('2') and not template.has('1', ignore_empty=True):
                pageinfo['vers'].append(j)
        
        if pageinfo['vers']:
            outputlist.append(pageinfo)


with open('misc/output.json', 'w') as outfile:
    json.dump(outputlist, outfile)