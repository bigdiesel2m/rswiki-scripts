import json
import mwparserfromhell
    

with open('scrape/contents_osw.json') as infile: #grab the >data<
    data_osw = json.load(infile)

outputlist = []
for i in range(len(data_osw)):
    if i%1000==0:
        print('current step:',i)
    page = data_osw[i]

    pageinfo = {
        'title': page['title'],
        'odds': [],
    }

    wikitext = mwparserfromhell.parse(page['contents'])
    rdt = wikitext.filter_templates(matches="RareDropTable")
    if rdt:
        rdt = rdt[0]
        if rdt.has('1'):
            pageinfo['odds'] = str(rdt.get('1').value)
            infobox = wikitext.filter_templates(matches="Infobox Monster")
            if infobox:
                infobox = infobox[0]
                if infobox.has('combat'):
                    pageinfo['combat'] = str(infobox.get('combat').value).strip('\n')
                elif infobox.has('combat1'):
                    pageinfo['combat'] = str(infobox.get('combat1').value).strip('\n')
            print(pageinfo)
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
