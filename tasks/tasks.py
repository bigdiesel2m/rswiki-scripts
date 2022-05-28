import csv
import json
import re

datalist = []
ignored = []

with open("tasks/data_test.tsv") as file:
    data = csv.reader(file, delimiter="\t")
    for row in data:
        msg = row[0].replace("<br>", " ")
        
        if (re.search("(USERNAME|How many)", msg)):
            ignored.append(msg)
        elif (re.search("Your new task is to kill [0-9]{1,3} .*\.", msg)): # NORMAL
            num = re.search('(?<=kill )[0-9]{1,3}', msg).group(0)
            mon = re.search('(?<=[0-9] ).*(?=\.)', msg).group(0)
            datalist.append(num + '\t' + mon + '\t' + row[1] + '\t' + row[2])
        elif (re.search("^Great", msg)): # GREAT
            num = re.search('(?<=kill )[0-9]{1,3}', msg).group(0)
            mon = re.search('(?<=[0-9] ).*', msg).group(0)
            datalist.append(num + '\t' + mon + '\t' + row[1] + '\t' + row[2])
        elif (re.search("You are to bring balance to [0-9]{1,3}.* (in|on|south) .*\.", msg)): # KONAR
            num = re.search('(?<=balance to )[0-9]{1,3}', msg).group(0)
            mon = re.search('(?<=[0-9] ).*(?= (in|on|south) )', msg).group(0)
            datalist.append(num + '\t' + mon + '\t' + row[1] + '\t' + row[2])
        else:
            ignored.append(msg)

print(len(datalist))
print(len(ignored))
with open('tasks/output.txt', 'w') as outfile:
    outfile.write('\n'.join(datalist))