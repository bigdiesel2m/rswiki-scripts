# This script converts the scraped contents into dicts, with the key for each dict being the pagename.
# This makes it easier to find matching pages based on the external/indicator templates

import json

rsc_dict = {} #set up empty dicts
rsw_dict = {}
osw_dict = {}

with open('scrape/contents_rsc.json') as infile: #open up files
    data_rsc = json.load(infile)

with open('scrape/contents_rsw.json') as infile:
    data_rsw = json.load(infile)

with open('scrape/contents_osw.json') as infile:
    data_osw = json.load(infile)

for i in range(len(data_rsc)): #convert from list to dict
    rsc_dict[data_rsc[i]['title']] = [data_rsc[i]['contents']]

for i in range(len(data_rsw)):
    rsw_dict[data_rsw[i]['title']] = [data_rsw[i]['contents']]

for i in range(len(data_osw)):
    osw_dict[data_osw[i]['title']] = [data_osw[i]['contents']]

with open('toplinks/contents_rsc_dict.json', 'w') as outfile: #export to a new json as a dict
    json.dump(rsc_dict, outfile)

with open('toplinks/contents_rsw_dict.json', 'w') as outfile:
    json.dump(rsw_dict, outfile)

with open('toplinks/contents_osw_dict.json', 'w') as outfile:
    json.dump(osw_dict, outfile)