#Logfile Parser
from string import split
from operator import itemgetter

def parseline(line):
	try:
		arr=split(line, "z_*")
		print(arr)
		time=arr[0]
		module=arr[1]
		urgency=arr[2]
		message=arr[3]

		parsedtime=split(time, "|")

		return(parsedtime[0], parsedtime[1], parsedtime[2], module, urgency, message)

	except:
		return None

Lines=[]
def parsefile(filepath):
	filep=open(filepath, "r")
	filed=filep.read()

	for line in split(filed, "\n"):
		try:
			Foo=parseline(line)
			if Foo!=None:
				(h, m, s, mod, lvl, msg) = Foo
				Lines.append([h, m, s, mod, lvl, msg])
		except:
			pass

def sortbyUrgency():
	foo=Lines
	sorted(foo, key=itemgetter(4))
	print("\n"*10)
	for x in foo:
		print x
	return foo

def printNice(lines):
	print("Typing")
	for line in lines:
		print(line[0]+":"+line[1]+":"+line[2]+" ("+line[3]+") "+line[4]+" - "+line[5])

def printListctl(lines, instance):
	for line in lines:
		instance.InsertStringItem(lines.index(line), "0"*(2-len(line[0]))+line[0]+":"+"0"*(2-len(line[1]))+line[1]+":"+"0"*(2-len(line[2]))+line[2])
		instance.SetStringItem(lines.index(line), 1, line[4])
		instance.SetStringItem(lines.index(line), 2, line[3])
		instance.SetStringItem(lines.index(line), 3, line[5])
		instance.SetItemData(lines.index(line), lines.index(line))