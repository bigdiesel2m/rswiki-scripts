import json
import re

regex = "dungeon"
exclude = "resource dungeon"

with open('scrape/contents_rsw.json') as infile: #grab the >data<
    data = json.load(infile)

outputlist = []
for i in range(len(data)):
    if i%1000==0:
        print('current step:',i)
    title = data[i]['title']
    if(re.search(regex, title)) and not (re.search(exclude, title)):
        outputlist.append(title)
    
outputstr = '\n'.join(outputlist)

with open('misc/name_results.txt', 'w') as outfile:
    outfile.write(outputstr)
