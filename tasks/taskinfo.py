import json
import matplotlib.pyplot as plt

with open('tasks/output.json') as infile:
    data = json.load(infile)

master = 'Turael'

for monster in data[master]:
    x = []
    y = []
    for key in data[master][monster]:
        x.append(int(key))
        y.append(data[master][monster][key])
    
    # plotting the points 
    plt.bar(x, y)
    
    # giving a title to my graph
    plt.title(master + ' - ' + monster)
    
    plt.show()