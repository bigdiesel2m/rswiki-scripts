import sys
import json
import math
import os.path
import glob

index = 11461
outlist = []

for file in glob.glob("dump/npc_defs/*.json"):
    with open(file) as infile:
        data_json = json.load(infile)
    if('id' in data_json and 'name' in data_json and 'models' in data_json):
        if(len(data_json['models']) > 5):
            outlist.append(str(data_json['id']) + '\t' + str(data_json['name']) + '\t' + str(len(data_json['models'])) + '\t' + str(min(data_json['models'])))
    else:
        print(file)
        

with open('npcmodels/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))