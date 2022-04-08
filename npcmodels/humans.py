import sys
import json
import math
import os.path
import glob

# configuration parameters
regenerate = False # set to true to regenerate NPC list before filtering
badnames = ['Zombie', 'Skeleton', 'Mummy', 'Goblin', 'Dwarf', 'Combat stone', 'Ork', 'TzHaar-Xil', 'TzHaar-Ket', 'Aviansie', 'Zombie pirate',]
badmodels = []

def common_member(a, b):
    if len(set(a).intersection(set(b))) > 0:
        return(True)
    return(False)

# this section either regenerates the list of models based on some broad filters or uses the existing list
outjson = []
if regenerate:
    for file in glob.glob("dump/npc_defs/*.json"):
        with open(file) as infile:
            data_json = json.load(infile)
        if('id' in data_json and 'name' in data_json and 'models' in data_json):
            if(len(data_json['models']) > 5):
                outjson.append({'id': data_json['id'], 'name': data_json['name'], 'models': data_json['models']})
        # else:
        #     print(data_json['id'])
    with open('npcmodels/output.json', 'w') as outfile:
        json.dump(outjson, outfile)
else:
    with open('npcmodels/output.json') as infile:
        outjson = json.load(infile)
print(len(outjson))

# this section adds some finer filters to pare down the list
outtxt = []
for i in range(len(outjson)):
    if common_member(badnames, [outjson[i]['name']]):
        continue
    elif common_member(badmodels, outjson[i]['models']):
        continue
    else:
        outtxt.append(str(outjson[i]['id']) + '\t' + str(outjson[i]['name']) + '\t' + str(len(outjson[i]['models'])))
print(len(outtxt))

with open('npcmodels/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outtxt))