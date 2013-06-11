#'Configfile' to Mapfile converter:

import textvalidator
import pickle
from string import split

File=raw_input("")
raw=open(File, "r").read()

#print(raw)

lines=split(raw, "\n")

Config={}
CurrentSection=None
CurrentSubSection=None

for line in lines:
	if line=="Mapfile:":
		pass

	elif len(line)==0:
		pass

	elif line[0]==" ":
		pass

	elif line[0]=="#":
		pass

	elif line[0]=="[":
		foo=line.replace("[", "").replace("]","")
		CurrentSection=foo
		#print(CurrentSection)
		Config[foo]={}

	elif line[0]=="{":
		foo=line.replace("{", "").replace("}","")
		CurrentSubSection=foo
		#print(CurrentSubSection)
		Config[CurrentSection][foo]={}

	elif "=" in line:
		foo=split(line, "=")
		Config[CurrentSection][CurrentSubSection][foo[0]]=textvalidator.convertToReal(foo[1])

print(pickle.dumps(Config))