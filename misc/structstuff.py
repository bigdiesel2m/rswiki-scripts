import json
import glob

outlist = []
for file in glob.glob("dump/enums/*.json"):
    with open(file) as infile:
        data_json = json.load(infile)
    if 816 in data_json["keys"]:
        outlist.append(str(data_json['id']))
        
with open('misc/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))