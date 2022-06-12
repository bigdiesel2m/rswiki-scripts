import json
import mwparserfromhell
import re

with open('scrape/drops_osw.json') as infile:
    data_osw = json.load(infile)

outlist = []
for i in range(len(data_osw)):
    if i % 100 == 0:
        print(i)
    page = data_osw[i]
    text = page['contents']
    wikicode = mwparserfromhell.parse(text)
    templates = wikicode.filter_templates()
    for template in templates:
        if template.name.matches(("DropsLine","DropsLineReward","DropsLineSkill")):
            name = ''
            quant = ''
            note = ''
            if not template.has("quantity") and not template.has("name"):
                name = 'missingname'
                quant = 'missingquant'
                note = 'bothproblem'
            elif not template.has("quantity") and template.has("name"):
                name = str(template["name"].value)
                quant = 'missingquant'
                note = 'quantproblem'
            elif not template.has("name") and template.has("quantity"):
                name = 'missingname'
                quant = str(template["quantity"].value)
                note = 'nameproblem'
            elif template.has("name") and template.has("quantity"):
                name = str(template["name"].value)
                quant = str(template["quantity"].value)
                quantre = re.compile(r'[0-9]+ ?-? ?[0-9]*')
                mo = quantre.findall(quant)
                if len(mo) == 0:
                    note = 'no quant match'
                if len(mo) == 1:
                    note = 'one quant match'
                if len(mo) > 1:
                    note = 'multiple quant matches'
            outlist.append(page['title'] + '\t' + name + '\t' + quant + '\t' + note)

with open('drops/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))
        