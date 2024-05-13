# Script to read in crowdsourced locations and convert into loclines for easy reading
import json

with open("misc\input.txt", 'r') as file:
	content = ''
	line = file.readline()
	
	while line:
		content += line
		line = file.readline()

linelist = content.split("\n")
print(linelist[0])

locdict = {}

# group npcs with same id/index/plane into dicts
for line in linelist:
	splitline = line.split("\t")
	lineid = splitline[0] + " - " + splitline[1] + " - " + splitline[4]
	if lineid in locdict:
		locdict[lineid] = locdict[lineid] + "|"+splitline[2]+","+splitline[3]
	else:
		locdict[lineid] = "|"+splitline[2]+","+splitline[3]

# convert dict entries into strings in a list
outlist = []
for key in locdict:
	outlist.append("{{LocLine|name = "+key+"|location = "+key+"|mapID = -1|plane = "+key[-1]+locdict[key]+"}}")

# prepend and append loctable templates
outlist = ["{{LocTableHead}}"] + outlist + ["{{LocTableBottom}}"]

with open('misc/output.txt', 'w') as outfile:
	outfile.write('\n'.join(outlist))