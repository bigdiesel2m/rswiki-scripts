import sys
import json
import math

with open('batcher/32627.json') as infile:
    data_json = json.load(infile)

batches = [] # empty list of batches, to be iterated upon

def check_batches(item):
    for j in range(len(batches)):
        if item['i'] == batches[j]['i'] and item['j'] == batches[j]['j']:
            return j
    return None

# loading objects into batches based on i,j grid
for i in range(len(data_json)):
    batch = check_batches(data_json[i])
    if batch != None:
        # if we have a batch with correct i,j add object to that batch
        batches[batch]['list'].append(data_json[i])
    else:
        # else create a new batch and add the object as the first member
        batches.append({'i': data_json[i]['i'], 'j': data_json[i]['j'], 'list': [data_json[i]]})

# now that we've batched stuff up, it's time to turn those into locline templates
outlist = []
for i in range(len(batches)):
    planelist = [[], [], [], []]
    for j in range(len(batches[i]['list'])):
        planelist[batches[i]['list'][j]['plane']].append(str(64*batches[i]['list'][j]['i'] + batches[i]['list'][j]['x']) + ',' + str(64*batches[i]['list'][j]['j'] + batches[i]['list'][j]['y']))
    for j in range(len(planelist)):
        if len(planelist[j]) > 0:
            planelist[j] = '|'.join(planelist[j])
            outlist.append('{{ObjectLocLine\n|name = Drapes\n|location = ' + str(batches[i]['i']) + ',' + str(batches[i]['j']) + ' - {{FloorNumber|uk=' + str(j) + '}}\n|members = Yes\n|mapID = -1\n|plane = ' + str(j) + '\n|' + planelist[j] + '\n|mtype = pin}}')

with open('batcher/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))