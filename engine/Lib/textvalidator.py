#Validator

from engine import shared, debug
from os.path import isfile
from string import split

def Validate(text, Vtype):
	texturefolder = "./media/materials/textures/"
	try:
		if type(Vtype) is list:
			print(Vtype)
			if text in Vtype:
				return text

		else:
			if Vtype=="file":
				if isfile(shared.wd+text) or isfile(texturefolder+text):
					return text

			if Vtype=="filelist":
				foo=split(text, ";")
				print(foo)
				if len(foo)!=0:
					for x in foo:
						if isfile(shared.wd+x) or isfile(texturefolder+x):
							print("isfile: "+x)
						else:
							return None
					return foo

			if Vtype=="vector2":
				foo=split(text.replace("(", "").replace(")", ""), ",")
				if len(foo)==2:
					return (foo[0],foo[1])

			if Vtype=="vector3":
				foo=split(text.replace("(", "").replace(")", ""), ",")
				if len(foo)==3:
					return (foo[0],foo[1],foo[2])

			if Vtype=="float":
				try:
					return float(text)
				except:
					pass

			if Vtype=="int":
				try:
					return int(text)
				except:
					pass

			if Vtype=="str":
				try:
					return str(text)
				except:
					pass

			if Vtype=="bool":
				try:
					return bool(text)
				except:
					pass

			if Vtype=="color":
				foo=split(text.replace("(", "").replace(")", ""), ",")
				if len(foo)==3:
					if foo[0]>=1 and foo[1]>=1 and foo[2]>=1:
						return (foo[0],foo[1],foo[2])
			return None
	except:
		return None

def convertConfig(config):
	realconfig=config
	for section, content in config.iteritems():
		for key, value in content.iteritems():
			realconfig[section][key]=convertToReal(value)
	return realconfig


def convertToReal(text):
	#Parsing Vector 2/3:
	if "," in text:
		try:
			foo=split(text.replace("(", "").replace(")", ""), ",")
			if len(foo)==3:
				return (foo[0],foo[1],foo[2])
			if len(foo)==2:
				return (foo[0],foo[1])
		except:
			pass


	#Parsing Lists:
	elif text[0]=="[" and text[len(Value)-1]=="]":
		try:
			return split(value.replace("[", "").replace("]",""),",")
		except:
			pass

	elif ";" in text:
		try:
			return split(text, ";")
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