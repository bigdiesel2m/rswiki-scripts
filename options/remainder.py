import json

with open('options/output.json') as infile:
	data = json.load(infile)

#outputlist = [itemlist, multboxlist, versionlist, verdiflist, weirdidlist, droplist, destroylist, otherlist]
#[8851, 6, 1219, 372, 383, 6517, 982, 591]
print(len(data))
data[1] = [element + '\tMultiple Infoboxes' for element in data[1]]
data[3] = [element + '\tVersion Differences' for element in data[3]]
data[4] = [element + '\tWeird ID Stuff' for element in data[4]]
data[7] = [element + '\tOther Issues' for element in data[7]]

outlist = [data[1], data[3], data[4], data[7]]
outlist = ['\n'.join(list) for list in outlist]
outtxt = '\n'.join(outlist)

with open('options/remainders.txt', 'w') as outfile:
	outfile.write(outtxt)