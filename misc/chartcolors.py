import json
import mwparserfromhell
import collections

with open('scrape/contents_osw.json') as infile: #grab the >data<
    data_osw = json.load(infile)

regenchartlist = False

if regenchartlist:
    chartlist = []
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
        allcharts = wikitext.filter_templates(matches=r"\{\{Skilling success chart")
        if allcharts:
            for chart in allcharts:
                chartlist.append(str(chart))
    with open('misc/chartlist.json', 'w') as outfile:
        json.dump(chartlist, outfile)
else:
	with open('misc/chartlist.json', 'r') as infile:
		chartlist = json.load(infile)

makecolorlist = True

if makecolorlist:
    colorlist = []
    for chart in chartlist:
        chart = mwparserfromhell.parse(chart).filter_templates()[0] # this loads the stringified template back in, parses it into wikitext, then gets it read as a template again
        # if chart.has('label') and "cut chance" in str(chart.get('label').value).lower():
        if chart.has('label'):
            for i in range(30):
                colorparam = 'color' + str(i)
                labelparam = 'label' + str(i)
                if chart.has(colorparam) and chart.has(labelparam):
                    colorlist.append(str(chart.get(labelparam).value) + " - " + str(chart.get(colorparam).value))
        
    with open('misc/output.json', 'w') as outfile:
        json.dump(colorlist, outfile) 
    
    colordict = (dict(collections.Counter(colorlist)))

    colorcounts = []
    for color in colordict:
        outstr = color + "\t" + str(colordict[color])
        outstr = outstr.replace('\n','(NEWLINE)').replace('\r','(RETURN)')
        colorcounts.append(outstr)

    with open('misc/output.txt', 'w') as outfile:
        outfile.write("\n".join(colorcounts))

makelabellist = True

if makelabellist:
    labeldict = {'other': []}
    labelstrings = ['cooking','mining','pickpocket','fishing chance','catch chance','cut chance']
    for label in labelstrings:
        labeldict[label] = []
    for chart in chartlist:
        chart = mwparserfromhell.parse(chart).filter_templates()[0] # this loads the stringified template back in, parses it into wikitext, then gets it read as a template again
        if chart.has('label') and chart.has('label2'):
            labelval = str(chart.get('label').value)
            labelcat = 'other'
            for label in labelstrings:
                if label in labelval.lower():
                    labelcat = label
            labeldict[labelcat].append(labelval)

    with open('misc/output.json', 'w') as outfile:
        json.dump(labeldict, outfile)

