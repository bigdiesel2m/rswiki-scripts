# Script used to convert graphical updates pages to use {{GraphicalUpdateTable}}

with open("misc\input.txt", 'r') as file:
	content = ''
	line = file.readline()
	
	while line:
		content += line
		line = file.readline()

linelist = content.split("\n")
columns = 1

outlist = []
breakcount = 0
filecount = 0
namecount = 0
lastlastbreak = 0
lastbreak = 0

for i in range(len(linelist)):
	if linelist[i] == "|-" or linelist[i][0:2] == "{|":
		breakcount = breakcount+1
		lastlastbreak = lastbreak
		lastbreak = i
	elif linelist[i][0:8] == "|[[File:":
		filecount  = filecount+1
		newline = "|{{$|name=" + linelist[i-lastbreak+lastlastbreak][1:] + "|files=" + linelist[i][1:] + "}}"
		outlist.append(newline)
	elif linelist[i][1:3] == "[[":
		namecount = namecount+1
	else:
		print(linelist[i])

if (len(linelist)-breakcount) == len(outlist)*2 + 1:
	outlist.insert(0,"{{GraphicalUpdateTable|columns=" + str(columns))
	outlist.append("}}")
	with open('misc/output.txt', 'w') as outfile:
		outfile.write('\n'.join(outlist))
else:
	print("miscount!")