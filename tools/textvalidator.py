#Validator

from string import split

def convertConfig(config):
	#This is where I learned that a Dict is NOT a datatype, but an object. I used 4 hours debugging why the original of this dict changed..
	coffin=config
	realconfig={}
	for section, content in coffin.iteritems():
		realconfig[section]={}
		for subsection, value in content.iteritems():
			#print(value)
			realconfig[section][subsection]=value

	#shared.Mapfile.checkYourPrivileges()

	for section, content in config.iteritems():
		for key, value in content.iteritems():
			realconfig[section][key]=convertToReal(value)

	#shared.Mapfile.checkYourPrivileges()
	return realconfig


def convertToReal(text):
	text=str(text)
	if "," in text:
		try:
			foo=split(text.replace("(", "").replace(")", "").replace("'", "").replace('"',""), ",")
			if len(foo)==4:
				return (foo[0],foo[1],foo[2],foo[3])
			if len(foo)==3:
				return (foo[0],foo[1],foo[2])
			if len(foo)==2:
				return (foo[0],foo[1])
		except:
			pass


	#Parsing Lists:
	elif text[0]=="[" and text[len(text)-1]=="]":
		try:
			return split(value.replace("[", "").replace("]",""),",")
		except:
			pass

	elif ";" in text:
		try:
			return split(text, ";")
		except:
			pass

	elif "'" in text:
		try:
			return int(text.replace("'",""))
		except:
			pass

	elif '"' in text:
		try:
			return int(text.replace('"',""))
		except:
			pass

	#Parsing Boolean:
	elif text.lower()=="true":
		return True
	elif text.lower()=="false":
		return False

	#Parsing numbers
	else:
		#Parsing Integer
		try:
			return int(text)
		except ValueError:
			pass

		#Parsing Float
		try:
			return float(text)
		except ValueError:
			pass

		#Parsing String
		try:
			return str(text)
		except:
			pass