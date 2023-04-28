import json
import mwparserfromhell

def toplinktemplate(contents):
    wikitext = mwparserfromhell.parse(contents)
    indicators = wikitext.filter_templates(matches=lambda t: t.name.matches('Indicators'))
    external = wikitext.filter_templates(matches=lambda t: t.name.matches('External'))
    if external:
        return external
    elif indicators:
        return indicators

with open('scrape/contents_rsw.json') as infile: #grab the >data<
    data_rsw = json.load(infile)
with open('toplinks/contents_rsw_dict.json') as infile:
    dict_rsw = json.load(infile)
with open('toplinks/contents_osw_dict.json') as infile:
    dict_osw = json.load(infile)

#for loop starts here-ish
outputlist = []
for i in range(len(data_rsw)):
    if i%1000==0:
        print('current step:',i)
    page = data_rsw[i]


    newpage = {
        'title': page['title'],
        'rsw_to_osw': '',
        'osw_to_rsw': '',
        'errors_rsw': [],
        'errors_osw': [],
    }

    toptemp = toplinktemplate(page['contents'])

    if toptemp:
        toptemp = toptemp[0]
        if toptemp.has('os'):
            newpage['rsw_to_osw'] = toptemp.get("os").value
        for j in range(4):
            if toptemp.has(str(j)):
                param = toptemp.get(str(j)).value
                if param == 'os':
                    newpage['rsw_to_osw'] = page['title']

        if newpage['rsw_to_osw']:
            newpage['rsw_to_osw'] = str(newpage['rsw_to_osw']).replace("_"," ")
            if newpage['rsw_to_osw'] in dict_osw:
                toptemp = toplinktemplate(dict_osw[newpage['rsw_to_osw']])
                if toptemp:
                    toptemp = toptemp[0]
                    if toptemp.has('rs'): #if it has an rs param, 
                        newpage['osw_to_rsw'] = str(toptemp.get("rs").value).replace("_"," ") #take that for os
                    for k in range(4):
                        if toptemp.has(str(k)):
                            param = toptemp.get(str(k)).value
                            if param == 'rs':
                                newpage['osw_to_rsw'] = newpage['rsw_to_osw']
                    if newpage['osw_to_rsw']:  #now that we have all the toplinks we're gonna find, do error checking
                        if newpage['osw_to_rsw'] != newpage['title']:
                            newpage['errors_osw'].append('Bad RSW Link')
                    else:
                        newpage['errors_osw'].append('Missing RSW Link')
                else:
                    newpage['errors_osw'].append('Missing Template')
            else:
                newpage['errors_rsw'].append('Bad OSW Link')
        else:
            newpage['errors_rsw'].append('Missing OSW Link')

    outputlist.append(newpage)

with open('toplinks/rsw_toplinks_analysis_results.json', 'w') as outfile:
    json.dump(outputlist, outfile)

justdata = []

for i in range(len(outputlist)):
    values = list(outputlist[i].values())
    for j in range(len(values)):
        values[j] = str(values[j])
    values = '\t'.join(values)
    justdata.append(values)

justdata = '\n'.join(justdata)

with open('toplinks/rsw_toplinks_analysis_results_converted.txt', 'w', encoding='utf-8') as outfile:
    outfile.write(justdata)
