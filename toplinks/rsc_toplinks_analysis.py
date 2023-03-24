#This script goes through each page on RSCW and analyzes its toplinks
#It starts by finding any pages that are linked to by a toplink on a RSCW page
#Then, it checks any toplinks on those pages to see where they're pointing
#This lets us build a list of links out of RSC, then compare them to links back to RSC and links between OSW and RSW
#Any mismatches in these lists get highlighted
#This script currently does not look through all pages on OSW and RSW to check their toplinks
#It only looks at pages on those two wikis that somehow link back to RSC, for now

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

with open('scrape/contents_rsc.json') as infile: #grab the >data<
    data_rsc = json.load(infile)
with open('toplinks/contents_rsc_dict.json') as infile:
    dict_rsc = json.load(infile)
with open('toplinks/contents_rsw_dict.json') as infile:
    dict_rsw = json.load(infile)
with open('toplinks/contents_osw_dict.json') as infile:
    dict_osw = json.load(infile)

#for loop starts here-ish
outputlist = []
for i in range(len(data_rsc)):
    if i%1000==0:
        print('current step:',i)
    page = data_rsc[i]


    newpage = {
        'title': page['title'],
        'rsc_to_rsw': '',
        'rsc_to_osw': '',
        'rsw_to_rsc': '',
        'osw_to_rsc': '',
        'rsw_to_osw': '',
        'osw_to_rsw': '',
        'errors_rsc': [],
        'errors_rsw': [],
        'errors_osw': []
    }

    toptemp = toplinktemplate(page['contents'])

    if toptemp:
        toptemp = toptemp[0]
        if toptemp.has('os'): #if it has an os param, 
            newpage['rsc_to_osw'] = toptemp.get("os").value #take that for os
        if toptemp.has('rs'): #if it has an rs param,
            newpage['rsc_to_rsw'] = toptemp.get("rs").value #take that for rs
        if toptemp.has('1'): #otherwise, iterate on possible numeric params for os or rs inputs
            param1 = toptemp.get("1").value
            if param1 == 'os':
                newpage['rsc_to_osw'] = page['title']
            elif param1 == 'rs':
                newpage['rsc_to_rsw'] = page['title']
        if toptemp.has('2'):
            param2 = toptemp.get("2").value
            if param2 == 'os':
                newpage['rsc_to_osw'] = page['title']
            elif param2 == 'rs':
                newpage['rsc_to_rsw'] = page['title']
        if toptemp.has('3'):
            param3 = toptemp.get("3").value
            if param3 == 'os':
                newpage['rsc_to_osw'] = page['title']
            elif param3 == 'rs':
                newpage['rsc_to_rsw'] = page['title']
        if toptemp.has('4'):
            param4 = toptemp.get("4").value
            if param4 == 'os':
                newpage['rsc_to_osw'] = page['title']
            elif param4 == 'rs':
                newpage['rsc_to_rsw'] = page['title']

        if newpage['rsc_to_rsw']: #if we have a rsw toplink
            newpage['rsc_to_rsw'] = str(newpage['rsc_to_rsw']).replace("_"," ")
            if newpage['rsc_to_rsw'] in dict_rsw: #if the toplink goes to a page on RSW
                toptemp = toplinktemplate(dict_rsw[newpage['rsc_to_rsw']]) #then get the toplinks for that page on RSW
                if toptemp:
                    toptemp = toptemp[0]
                    if toptemp.has('os'): #if it has an os param, 
                        newpage['rsw_to_osw'] = str(toptemp.get("os").value).replace("_"," ") #take that for os
                    if toptemp.has('rsc'): #if it has an rsc param,
                        newpage['rsw_to_rsc'] = str(toptemp.get("rsc").value).replace("_"," ") #take that for rsc
                    if toptemp.has('1'): #otherwise, iterate on possible numeric params for os or rsc inputs
                        param1 = toptemp.get("1").value
                        if param1 == 'os':
                            newpage['rsw_to_osw'] = newpage['rsc_to_rsw']
                        elif param1 == 'rsc':
                            newpage['rsw_to_rsc'] = newpage['rsc_to_rsw']
                    if toptemp.has('2'):
                        param2 = toptemp.get("2").value
                        if param2 == 'os':
                            newpage['rsw_to_osw'] = newpage['rsc_to_rsw']
                        elif param2 == 'rsc':
                            newpage['rsw_to_rsc'] = newpage['rsc_to_rsw']
                    if toptemp.has('3'):
                        param3 = toptemp.get("3").value
                        if param3 == 'os':
                            newpage['rsw_to_osw'] = newpage['rsc_to_rsw']
                        elif param3 == 'rsc':
                            newpage['rsw_to_rsc'] = newpage['rsc_to_rsw']
                    if toptemp.has('4'):
                        param4 = toptemp.get("4").value
                        if param4 == 'os':
                            newpage['rsw_to_osw'] = newpage['rsc_to_rsw']
                        elif param4 == 'rsc':
                            newpage['rsw_to_rsc'] = newpage['rsc_to_rsw']
                    if newpage['rsw_to_rsc']:  #now that we have all the toplinks we're gonna find, do error checking
                        if newpage['rsw_to_rsc'] != newpage['title']:
                            newpage['errors_rsw'].append('Bad RSC Link')
                    else:
                        newpage['errors_rsw'].append('Missing RSC Link')
                    if not newpage['rsw_to_osw']:
                        newpage['errors_rsw'].append('Missing OSW Link')
                else:
                    newpage['errors_rsw'].append('Missing Template')
            else:
                newpage['errors_rsc'].append('Bad RSW Link')
        else:
            newpage['errors_rsc'].append('Missing RSW Link')

        if newpage['rsc_to_osw']: #if we have a osw toplink
            newpage['rsc_to_osw'] = str(newpage['rsc_to_osw']).replace("_"," ")
            if newpage['rsc_to_osw'] in dict_osw: #if the toplink goes to a page on OSW
                toptemp = toplinktemplate(dict_osw[newpage['rsc_to_osw']]) #then get the toplinks for that page on OSW
                if toptemp:
                    toptemp = toptemp[0]
                    if toptemp.has('rs'): #if it has an rs param, 
                        newpage['osw_to_rsw'] = str(toptemp.get("rs").value).replace("_"," ") #take that for os
                    if toptemp.has('rsc'): #if it has an rsc param,
                        newpage['osw_to_rsc'] = str(toptemp.get("rsc").value).replace("_"," ") #take that for rsc
                    if toptemp.has('1'): #otherwise, iterate on possible numeric params for os or rsc inputs
                        param1 = toptemp.get("1").value
                        if param1 == 'rs':
                            newpage['osw_to_rsw'] = newpage['rsc_to_osw']
                        elif param1 == 'rsc':
                            newpage['osw_to_rsc'] = newpage['rsc_to_osw']
                    if toptemp.has('2'):
                        param2 = toptemp.get("2").value
                        if param2 == 'rs':
                            newpage['osw_to_rsw'] = newpage['rsc_to_osw']
                        elif param2 == 'rsc':
                            newpage['osw_to_rsc'] = newpage['rsc_to_osw']
                    if toptemp.has('3'):
                        param3 = toptemp.get("3").value
                        if param3 == 'rs':
                            newpage['osw_to_rsw'] = newpage['rsc_to_osw']
                        elif param3 == 'rsc':
                            newpage['osw_to_rsc'] = newpage['rsc_to_osw']
                    if toptemp.has('4'):
                        param4 = toptemp.get("4").value
                        if param4 == 'rs':
                            newpage['osw_to_rsw'] = newpage['rsc_to_osw']
                        elif param4 == 'rsc':
                            newpage['osw_to_rsc'] = newpage['rsc_to_osw']
                    if newpage['osw_to_rsc']:  #now that we have all the toplinks we're gonna find, do error checking
                        if newpage['osw_to_rsc'] != newpage['title']:
                            newpage['errors_osw'].append('Bad RSC Link')
                    else:
                        newpage['errors_osw'].append('Missing RSC Link')
                    if not newpage['osw_to_rsw']:
                        newpage['errors_osw'].append('Missing RSW Link')
                else:
                    newpage['errors_osw'].append('Missing Template')
            else:
                newpage['errors_rsc'].append('Bad OSW Link')
        else:
            newpage['errors_rsc'].append('Missing OSW Link')
    else:
        newpage['errors_rsc'].append('Missing Template')

    if newpage['osw_to_rsw']: #one last set of checks for rsw/osw toplinks
        if newpage['osw_to_rsw'] != newpage['rsc_to_rsw']:
            newpage['errors_osw'].append('Toplink Mismatch')

    if newpage['rsw_to_osw']:
        if newpage['rsw_to_osw'] != newpage['rsc_to_osw']:
            newpage['errors_rsw'].append('Toplink Mismatch')

    outputlist.append(newpage)

with open('toplinks/rsc_toplinks_analysis_results.json', 'w') as outfile:
    json.dump(outputlist, outfile)