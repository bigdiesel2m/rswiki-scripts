import json
import matplotlib.pyplot as plt

with open('tasks/output.json') as infile:
    data = json.load(infile)

master = 'Nieve'
monlist = []
for mon in data[master]:
    monlist.append(mon)
monlist.sort()

for monster in monlist:
    monster = 'TzHaar' # USED FOR FINDING SPECIFIC INFO
    x = []
    y = []
    for key in data[master][monster]:
        x.append(int(key))
        y.append(data[master][monster][key])
    
    plt.bar(x, y)
    plt.title(master + ' - ' + monster)
    
    plt.show()
    exit(0) # USED FOR FINDING SPECIFIC INFO