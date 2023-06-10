import json
import mwparserfromhell

with open('scrape/contents_osw.json') as infile: #grab the >data<
    data_osw = json.load(infile)

namelist = []
outputlist = []
for i in range(len(data_osw)):
    if i%1000==0:
        print('current step:',i)
    name = data_osw[i]['title'].lower()
    if name in namelist:
        outputlist.append(name)
    else:
        namelist.append(name)

with open('misc/output.json', 'w') as outfile:
    json.dump(outputlist, outfile)