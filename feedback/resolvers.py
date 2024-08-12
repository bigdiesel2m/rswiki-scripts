## Updated script for finding and counting users that resolve feedback
## Input is an XML file, obtained from https://runescape.wiki/w/Special:Export
## Special:Export params are: Add pages from "Category:Pages with resolved feedback", uncheck "Include only the current revision, not the full history" (because we want histories)

import xml.etree.ElementTree as ET
import mwparserfromhell
from collections import Counter

tree = ET.parse('feedback/wiki.xml')
root = tree.getroot()

userlist = []

for page in root.iter('{http://www.mediawiki.org/xml/export-0.11/}page'):
	# print(page.find('{http://www.mediawiki.org/xml/export-0.11/}title').text) # Print command for debugging
	oldfeedbackdict = {} # Creates an empty dict for holding feedback IDs and status
	for revision in page.iter('{http://www.mediawiki.org/xml/export-0.11/}revision'):
		wikitext = mwparserfromhell.parse(revision.find('{http://www.mediawiki.org/xml/export-0.11/}text').text)
		feedbacks = wikitext.filter_templates(matches='{{Feedback')

		newfeedbackdict = {}
		for template in feedbacks:
			if 'id' in template and 'resolved' in template:
				newfeedbackdict[template.get('id').value.strip()] = template.get('resolved').value.strip().lower()
		
		for feedback in newfeedbackdict:
			if newfeedbackdict[feedback] == 'yes' and (feedback in oldfeedbackdict) and oldfeedbackdict[feedback] == 'no':
				contribinfo = revision.find('{http://www.mediawiki.org/xml/export-0.11/}contributor')
				if contribinfo.find('{http://www.mediawiki.org/xml/export-0.11/}username') != None:
					userlist.append(contribinfo.find('{http://www.mediawiki.org/xml/export-0.11/}username').text)
				elif contribinfo.find('{http://www.mediawiki.org/xml/export-0.11/}ip') != None:
					userlist.append(contribinfo.find('{http://www.mediawiki.org/xml/export-0.11/}ip').text)
		oldfeedbackdict = newfeedbackdict


counted = Counter(userlist)

outlist = []
for user in counted:
	outlist.append(user + "\t" + str(counted[user]))

with open('feedback/resolvercount.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))