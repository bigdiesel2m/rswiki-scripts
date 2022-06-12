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
            if template.has("name") and template.has("quantity"):
                name = str(template["name"].value)
                quant = str(template["quantity"].value)
                quantre = re.compile(r'[0-9]+ ?-? ?[0-9]*')
                mo = quantre.findall(quant)
                if len(mo) == 1:
                    notere = re.compile(r' ?\(?noted?\)?')
                    notecheck = notere.findall(quant)
                    if len(notecheck) == 0:
                        quant2 = mo[0]
                        quant2re = re.compile(r'[0-9]+')
                        mo2 = quant2re.findall(quant2)
                        quantmax = 0
                        if len(mo2) == 1:
                            quantmax = mo2[0]
                        elif len(mo2) == 2:
                            quantmax = mo2[1]
                        if int(quantmax) > 1:
                            itemre = re.compile(r'Coins| rune$| bolt| arrow| seed$| knife| bait$| dart|Swamp tar|Cannonball|Feather| thrownaxe|avelin| nails$|Swamp paste|Tokkul|Numulite| firelighter| shards| teleport')
                            itemcheck = itemre.findall(name)
                            if len(itemcheck) == 0:
                                outlist.append(page['title'] + '\t' + name + '\t' + quant + '\t' + quantmax)

print(len(outlist))
with open('drops/output.txt', 'w') as outfile:
    outfile.write('\n'.join(outlist))
        