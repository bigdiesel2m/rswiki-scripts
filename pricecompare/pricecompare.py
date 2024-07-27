import json

# LOAD IN THE FILES
with open('pricecompare/geprices.json', 'r') as infile:
	geprices = json.load(infile)

with open('pricecompare/volumes.json', 'r') as infile:
	volumes = json.load(infile)

regenrealtimedict = True
if regenrealtimedict: # CONVERT REALTIME DATA INTO SIMPLER DICT
	with open('pricecompare/latest.json', 'r') as infile:
		latest = json.load(infile)
	with open('pricecompare/mapping.json', 'r') as infile:
		mapping = json.load(infile)

	realtimedict = {}
	for item in mapping:
		itemname = item['name']
		itemid = item['id']
		if str(itemid) in latest['data']:
			if 'high' in latest['data'][str(itemid)] and 'low' in latest['data'][str(itemid)]:
				realtimedict[itemname] = {
					'high': latest['data'][str(itemid)]['high'],
					'low': latest['data'][str(itemid)]['low'],
				}

	with open('pricecompare/realtimedict.json', 'w') as outfile:
		json.dump(realtimedict, outfile) 
else:
	with open('pricecompare/realtimedict.json', 'r') as infile:
		realtimedict = json.load(infile)

norealtime = []
for item in geprices:
	if item in realtimedict:
		realtimedict[item]['ge'] = geprices[item]
	else:
		norealtime.append(item)
for item in volumes:
	if item in realtimedict:
		realtimedict[item]['volume'] = volumes[item]

outlist = []
nogemaybe = []
for item in realtimedict:
	if len(realtimedict[item]) == 4:
		itemlist = [str(item),str(realtimedict[item]['ge']),str(realtimedict[item]['volume']),str(realtimedict[item]['high']),str(realtimedict[item]['low'])]
		outlist.append('\t'.join(itemlist))
	else:
		nogemaybe.append(item)

with open('pricecompare/output.txt', 'w') as outfile:
	outfile.write("\n".join(outlist))

# print(norealtime)
# print(nogemaybe)