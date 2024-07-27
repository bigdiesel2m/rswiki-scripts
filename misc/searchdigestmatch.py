import json
import glob
import re

digest = open("misc/searchdigest.txt", "r")
digestlist = digest.read().split("\n")

pattern = r' \([0-9]*\)'

cleanlist = []
for item in digestlist:
	item = re.sub(pattern, '', item)
	cleanlist.append(item)

print(cleanlist)

outputlist = []
i = 0
for file in glob.glob("dump/object_defs/*.json"):
	with open(file) as infile:
		i = i+1
		if i%1000==0:
			print('current step:',i)
		objname = json.load(infile)['name']
		if(objname in cleanlist):
			outputlist.append(objname)

with open('misc/output.txt', 'w') as outfile:
    outfile.write('\n'.join(list(set(outputlist))))
