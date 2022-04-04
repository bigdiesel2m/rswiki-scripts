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
    if i%50==0: print('current step:',i)

    batch = check_batches(data_json[i])
    if batch != None:
        batches[batch]['list'].append(data_json[i])
    else:
        # else create a new batch and add the object as the first member
        batches.append({'i': data_json[i]['i'], 'j': data_json[i]['j'], 'list': [data_json[i]]})

print(len(batches))