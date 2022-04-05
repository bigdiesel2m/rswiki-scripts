import sys
import json
import math

# configuration paramaters
ids = ['29983', '29984', '29985']
name = 'Lizardman corpse'
threshold = 0 # threshold for multi-chunk batches; set to 0 for separate chunks
outtype = 'locline' # set to 'locline' for locline output, otherwise outputs standard map

# empty lists for later use
batches = []
superbatches = []
data_json = []

for i in range(len(ids)):
    filename = 'batcher/' + ids[i] + '.json'
    with open(filename) as infile:
        data_json = data_json + json.load(infile)

# define functions for batching, could maybe be combined into one function
def check_batches(item):
    for j in range(len(batches)):
        if item['i'] == batches[j]['i'] and item['j'] == batches[j]['j']:
            return j
    return None

def check_super(batch):
    for j in range(len(superbatches)):
        if (abs(batch['i'] - superbatches[j]['i_min']) <= threshold or abs(batch['i'] - superbatches[j]['i_max']) <= threshold) and (abs(batch['j'] - superbatches[j]['j_min']) <= threshold or abs(batch['j'] - superbatches[j]['j_max']) <= threshold):
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

# optional, grouping batches based on configurable threshold
if threshold > 0:
    for i in range(len(batches)):
        superbatch = check_super(batches[i])
        if superbatch != None:
            superbatches[superbatch]['list'] = superbatches[superbatch]['list'] + batches[i]['list']
            superbatches[superbatch]['i_min'] = min(superbatches[superbatch]['i_min'], batches[i]['i'])
            superbatches[superbatch]['i_max'] = max(superbatches[superbatch]['i_max'], batches[i]['i'])
            superbatches[superbatch]['j_min'] = min(superbatches[superbatch]['j_min'], batches[i]['j'])
            superbatches[superbatch]['j_max'] = max(superbatches[superbatch]['j_max'], batches[i]['j'])
        else:
            superbatches.append({'i': batches[i]['i'], 'i_min': batches[i]['i'], 'i_max': batches[i]['i'], 'j': batches[i]['j'], 'j_min': batches[i]['j'], 'j_max': batches[i]['j'], 'list': batches[i]['list']})
    batches = superbatches


# now that we've batched stuff up, it's time to turn those into locline templates
outlist = []
for i in range(len(batches)):
    planelist = [[], [], [], []]
    for j in range(len(batches[i]['list'])):
        planelist[batches[i]['list'][j]['plane']].append(str(64*batches[i]['list'][j]['i'] + batches[i]['list'][j]['x']) + ',' + str(64*batches[i]['list'][j]['j'] + batches[i]['list'][j]['y']))
    for j in range(len(planelist)):
        if len(planelist[j]) > 0:
            planelist[j] = '|'.join(planelist[j])
            if outtype == 'locline':
                outlist.append('{{ObjectLocLine\n|name = ' + name + '\n|location = ' + str(batches[i]['i']) + ',' + str(batches[i]['j']) + ' - {{FloorNumber|uk=' + str(j) + '}}\n|members = Yes\n|mapID = -1\n|plane = ' + str(j) + '\n|' + planelist[j] + '\n|mtype = pin}}')
            else:
                outlist.append('{{Map|name = ' + name + '|mapID = -1|plane = ' + str(j) + '|' + planelist[j] + '|mtype = pin}}')


with open('batcher/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))