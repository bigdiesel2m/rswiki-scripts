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

outlist = []
for i in range(len(batches)):
    list_0 = []
    list_1 = []
    list_2 = []
    list_3 = []
    for j in range(len(batches[i]['list'])):
        print(batches[i]['list'][j])
        if batches[i]['list'][j]['plane'] == 0:
            list_0.append(str(64*batches[i]['list'][j]['i'] + batches[i]['list'][j]['x']) + ',' + str(64*batches[i]['list'][j]['j'] + batches[i]['list'][j]['y']))
        elif batches[i]['list'][j]['plane'] == 1:
            list_1.append(str(64*batches[i]['list'][j]['i'] + batches[i]['list'][j]['x']) + ',' + str(64*batches[i]['list'][j]['j'] + batches[i]['list'][j]['y']))
        elif batches[i]['list'][j]['plane'] == 2:
            list_2.append(str(64*batches[i]['list'][j]['i'] + batches[i]['list'][j]['x']) + ',' + str(64*batches[i]['list'][j]['j'] + batches[i]['list'][j]['y']))
        elif batches[i]['list'][j]['plane'] == 3:
            list_3.append(str(64*batches[i]['list'][j]['i'] + batches[i]['list'][j]['x']) + ',' + str(64*batches[i]['list'][j]['j'] + batches[i]['list'][j]['y']))
