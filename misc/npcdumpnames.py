import json
import glob
import re

p = re.compile('[Ii]ce [Tt]roll')
outjson = []

i = 0
for file in glob.glob("dump/npc_defs/*.json"):
    if i % 100 == 0:
        print(i)
    i = i + 1

    with open(file) as infile:
        data_json = json.load(infile)
    if('id' in data_json and 'name' in data_json):
        if(p.search(data_json['name'])):
            outjson.append(str(data_json['id']) + '\t' + str(data_json['name']))

with open('misc/output.json', 'w') as outfile:
    json.dump(outjson, outfile)
print(len(outjson))

with open('misc/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outjson))