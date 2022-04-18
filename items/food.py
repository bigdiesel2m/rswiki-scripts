import json
import glob

outlist = []
for file in glob.glob("dump/item_defs/*.json"):
    with open(file) as infile:
        data_json = json.load(infile)
    if 'Eat' in data_json["interfaceOptions"]:
        outlist.append(str(data_json['id']) + '\t' + str(data_json['name']) + '\tEat')
    if 'Drink' in data_json["interfaceOptions"]:
        outlist.append(str(data_json['id']) + '\t' + str(data_json['name']) + '\tDrink')
    if 'Guzzle' in data_json["interfaceOptions"]:
        outlist.append(str(data_json['id']) + '\t' + str(data_json['name']) + '\tGuzzle')
        
with open('items/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))