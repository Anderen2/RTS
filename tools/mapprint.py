#Mapfile printer:

import pickle

mapname=raw_input("Mapfile: ")

mapfile=open("Data/Map/"+mapname, "r")
structure=pickle.loads(mapfile.read())

for section, content in structure.iteritems():
	print("\n["+section+"]")

	for key, value in content.iteritems():

		if type(value) == dict:
			#If the section has an subsection
			print("\n{"+str(key)+"}")

			for key2, value2 in value.iteritems():
				print(str(key2)+"="+str(value2))

		else:
			print(str(key)+"="+str(value))