import sys
import json
import math
import os.path
import glob

# configuration parameters
regenerate = True # set to true to regenerate NPC list before filtering

# this section either regenerates the list of models based on some broad filters or uses the existing list
i = 0
outjson = []
if regenerate:
    for file in glob.glob("dump/npc_defs/*.json"):
        if i % 100 == 0:
            print(i)
        i = i + 1

        with open(file) as infile:
            data_json = json.load(infile)
        if('id' in data_json and 'chatheadModels' in data_json):
            if(20271 in data_json['chatheadModels']):
                outjson.append({'id': data_json['id'], 'chatheadModels': data_json['chatheadModels']})

    with open('npcmodels/output.json', 'w') as outfile:
        json.dump(outjson, outfile)
else:
    with open('npcmodels/output.json') as infile:
        outjson = json.load(infile)
print(len(outjson))

# this section adds some finer filters to pare down the list
outtxt = []
for i in range(len(outjson)):
    outtxt.append(str(outjson[i]['id']) + '\t' + str(len(outjson[i]['chatheadModels'])))
print(len(outtxt))

with open('npcmodels/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outtxt))