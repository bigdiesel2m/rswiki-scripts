import sys
import json
import math

with open('batcher/32627.json') as infile:
    data_json = json.load(infile)

# print(data_json[1]['i'])
batches = [] # empty list of batches, to be iterated upon

# loading objects into batches based on i,j grid
for i in range(len(data_json)):
    if i%50==0: print('current step:',i)
    batched = False
    for j in range(len(batches)):
        if data_json[i]['i'] == batches[j]['i'] and data_json[i]['j'] == batches[j]['j']:
            # if the object's i,j match an existing batch, load it into that batch
            batches[j]['list'].append(data_json[i])
            batched = True
    if batched == False:
        # else create a new batch and add the object as the first member
        batches.append({'i': data_json[i]['i'], 'j': data_json[i]['j'], 'list': [data_json[i]]})
        print("new batch created")

print(len(batches))