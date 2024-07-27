import json
import glob

outlist = []
for file in glob.glob("dump/npc_defs/*.json"):
    with open(file) as infile:
        data_json = json.load(infile)
    # if 'chatheadModels' in data_json and not 'models' in data_json:
    if 'models' in data_json and 25362 in data_json['models']:
        # print(data_json['id'])
        # print(data_json['name'])
        outlist.append(str(data_json['name']))
        
with open('misc/output.txt', 'w') as outfile:
    outfile.write(','.join(outlist))