import json
import glob

outputlist = []
i = 0
for file in glob.glob("dump/object_defs/*.json"):
    if i % 1000 == 0:
        print('Progress: ' + str(i))
    i = i + 1

    with open(file) as infile:
        data_json = json.load(infile)
        if ('id' in data_json and 'name' in data_json):
            if len(data_json['name']) > 0 and data_json['name'][0].islower() and not data_json['name'] == "null":
                outputlist.append([data_json['id'], data_json['name']])

with open('misc/output.json', 'w') as outfile:
    json.dump(outputlist, outfile)