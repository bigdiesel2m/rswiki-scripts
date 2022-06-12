import csv
import json
import matplotlib.pyplot as plt

datar = {}
datac = {}
with open("drops/gauntletdata.tsv") as file:
    data = csv.reader(file, delimiter="\t")
    for row in data:
        if row[1] == "Crystal shards":
            if row[2] not in datar:
                datar[row[2]] = int(row[3])
            else:
                datar[row[2]] = int(datar[row[2]]) + int(row[3])
        elif row[1] == "Corrupted shards":
            if row[2] not in datac:
                datac[row[2]] = int(row[3])
            else:
                datac[row[2]] = int(datac[row[2]]) + int(row[3])

outjson = datac
with open('drops/output.json', 'w') as outfile:
    json.dump(outjson, outfile)

x = []
y = []
for key in outjson:
    x.append(int(key))
    y.append(int(outjson[key]))

plt.bar(x, y)
plt.show()