import json
import mwparserfromhell

def topclean(toplink):
    toplink = str(toplink)
    toplink = toplink.replace("_"," ")
    toplink = toplink[0].upper() + toplink[1:]
    return toplink

def toplinktemplate(contents):
    wikitext = mwparserfromhell.parse(contents)
    indicators = wikitext.filter_templates(matches=lambda t: t.name.matches('Indicators'))
    external = wikitext.filter_templates(matches=lambda t: t.name.matches('External'))
    if external:
        return external
    elif indicators:
        return indicators

with open('scrape/contents_osw.json') as infile: #grab the >data<
    data_osw = json.load(infile)
with open('toplinks/contents_rsc_dict.json') as infile:
    dict_rsc = json.load(infile)
with open('toplinks/contents_rsw_dict.json') as infile:
    dict_rsw = json.load(infile)
with open('toplinks/contents_osw_dict.json') as infile:
    dict_osw = json.load(infile)

#for loop starts here-ish
outputlist = []
for i in range(len(data_osw)):
    if i%1000==0:
        print('current step:',i)
    page = data_osw[i]


    newpage = {
        'title': page['title'],
        'osw_to_rsw': '',
        'osw_to_rsc': '',
        'rsw_to_osw': '',
        'rsc_to_osw': '',
        'rsw_to_rsc': '',
        'rsw_to_rsc': '',
        'rsc_to_rsw': '',
        'errors_osw': [],
        'errors_rsw': [],
        'errors_rsc': []
    }

    toptemp = toplinktemplate(page['contents'])

    if toptemp:
        toptemp = toptemp[0]
        if toptemp.has('rs'):
            newpage['osw_to_rsw'] = toptemp.get("rs").value
        if toptemp.has('rsc'):
            newpage['osw_to_rsc'] = toptemp.get("rsc").value
        for j in range(4):
            if toptemp.has(str(j)):
                param = toptemp.get(str(j)).value
                if param == 'rs':
                    newpage['osw_to_rsw'] = page['title']
                elif param == 'rsc':
                    newpage['osw_to_rsc'] = page['title']

        if newpage['osw_to_rsw']:
            newpage['osw_to_rsw'] = topclean(newpage['osw_to_rsw'])
            if newpage['osw_to_rsw'] in dict_rsw:
                toptemp = toplinktemplate(dict_rsw[newpage['osw_to_rsw']])
                if toptemp:
                    toptemp = toptemp[0]
                    if toptemp.has('os'): #if it has an os param, 
                        newpage['rsw_to_osw'] = topclean(toptemp.get("os").value)
                    if toptemp.has('rsc'): #if it has an rsc param,
                        newpage['rsw_to_rsc'] = topclean(toptemp.get("rsc").value)
                    for k in range(4):
                        if toptemp.has(str(k)):
                            param = toptemp.get(str(k)).value
                            if param == 'os':
                                newpage['rsw_to_osw'] = newpage['osw_to_rsw']
                            elif param == 'rsc':
                                newpage['rsw_to_rsc'] = newpage['osw_to_rsw']
                    if newpage['rsw_to_osw']:  #now that we have all the toplinks we're gonna find, do error checking
                        if newpage['rsw_to_osw'] != newpage['title']:
                            newpage['errors_rsw'].append('Bad OSW Link')
                    else:
                        newpage['errors_rsw'].append('Missing OSW Link')
                    if not newpage['rsw_to_rsc']:
                        newpage['errors_rsw'].append('Missing RSC Link')
                else:
                    newpage['errors_rsw'].append('Missing Template')
            else:
                newpage['errors_osw'].append('Bad RSW Link')
        else:
            newpage['errors_osw'].append('Missing RSW Link')

        if newpage['osw_to_rsc']:
            newpage['osw_to_rsc'] = topclean(newpage['osw_to_rsc'])
            if newpage['osw_to_rsc'] in dict_rsc:
                toptemp = toplinktemplate(dict_rsc[newpage['osw_to_rsc']])
                if toptemp:
                    toptemp = toptemp[0]
                    if toptemp.has('os'):
                        newpage['rsc_to_osw'] = topclean(toptemp.get("os").value)
                    if toptemp.has('rs'):
                        newpage['rsc_to_rsw'] = topclean(toptemp.get("rs").value)
                    for k in range(4):
                        if toptemp.has(str(k)):
                            param = toptemp.get(str(k)).value
                            if param == 'os':
                                newpage['rsc_to_osw'] = newpage['osw_to_rsc']
                            elif param == 'rs':
                                newpage['rsc_to_rsw'] = newpage['osw_to_rsc']
                    if newpage['rsc_to_osw']:  #now that we have all the toplinks we're gonna find, do error checking
                        if newpage['rsc_to_osw'] != newpage['title']:
                            newpage['errors_rsw'].append('Bad OSW Link')
                    else:
                        newpage['errors_rsc'].append('Missing OSW Link')
                    if not newpage['rsc_to_rsw']:
                        newpage['errors_rsc'].append('Missing RSW Link')
                else:
                    newpage['errors_rsc'].append('Missing Template')
            else:
                newpage['errors_osw'].append('Bad RSC Link')
        else:
            newpage['errors_osw'].append('Missing RSC Link')
    else:
        newpage['errors_osw'].append('Missing Template')

    if newpage['rsw_to_rsc']:
        if newpage['rsw_to_rsc'] != newpage['osw_to_rsc']:
            newpage['errors_rsw'].append('Toplink Mismatch')

    if newpage['rsc_to_rsw']:
        if newpage['rsc_to_rsw'] != newpage['osw_to_rsw']:
            newpage['errors_rsc'].append('Toplink Mismatch')

    outputlist.append(newpage)

with open('toplinks/osw_toplinks_analysis_results.json', 'w') as outfile:
    json.dump(outputlist, outfile)

justdata = []

for i in range(len(outputlist)):
    values = list(outputlist[i].values())
    for j in range(len(values)):
        values[j] = str(values[j])
    values = '\t'.join(values)
    justdata.append(values)

justdata = '\n'.join(justdata)

with open('toplinks/osw_toplinks_analysis_results_converted.txt', 'w') as outfile:
    outfile.write(justdata)