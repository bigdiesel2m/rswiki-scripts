import json
import glob

outputlist = []
i = 0
for file in glob.glob("dump/item_defs/*.json"):
    if i % 1000 == 0:
        print('Progress: ' + str(i))
    i = i + 1

    with open(file) as infile:
        data_json = json.load(infile)
        if ('id' in data_json and 'name' in data_json and 'params' in data_json):
            if ('295' in data_json['params']):
                outputlist.append(str(data_json['id']) + '\t' + str(data_json['name']) + '\t' + str(data_json['params']))

with open('misc/output.json', 'w') as outfile:
    json.dump(outputlist, outfile)

with open('misc/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outputlist))