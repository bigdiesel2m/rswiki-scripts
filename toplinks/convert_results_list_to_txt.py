#This script converts the results from a json to a txt file
#This makes it easy to import the results into Google Sheets to sort and examine there

import json

with open('toplinks/rsc_toplinks_analysis_results.json') as infile: #open up files
    results_list = json.load(infile)

justdata = []

for i in range(len(results_list)):
    values = list(results_list[i].values())
    for j in range(len(values)):
        values[j] = str(values[j])
    values = '\t'.join(values)
    justdata.append(values)

justdata = '\n'.join(justdata)

with open('toplinks/rsc_toplinks_analysis_results_converted.txt', 'w') as outfile:
    outfile.write(justdata)
