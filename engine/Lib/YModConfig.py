#Libmodule - YModConfigFile Loader

from engine import debug, shared
from engine.shared import DPrint
from os import listdir
from os.path import isfile, join
from string import split

class Parser():
	def __init__(self, filesfolders, ext):
		self.filesfolders=filesfolders
		self.ext=ext

	def start(self):
		return self.ReadEntitys()

	def ReadEntitys(self):
		DPrint("YModConfigLoader",1,"Reading Files..")
		#FilePath=self.filesfolders

		if type(self.filesfolders) is list:
			FilePath=""
			Files=self.filesfolders
		elif type(self.filesfolders) is str:
			if self.filesfolders[len(self.filesfolders)-1]=="/" or self.filesfolders[len(self.filesfolders)-1]=="\\":
				Files=[]
				FilePath=self.filesfolders
				for f in listdir(FilePath):
					if isfile(join(FilePath,f)):
						if f[len(f)-len(self.ext):]==self.ext:
							Files.append(f)
			else:
				FilePath=""
				Files=[self.filesfolders]
		else:
			DPrint("YModConfigLoader",3,"Error parsing argument of type: "+str(type(self.filesfolders)))
			return False

		self.EntDict={}
		for x in Files:
			f=open(join(FilePath,x),"r")
			Lines=f.readlines()
			for line in Lines:
				if line==Lines[0]:
					Name=line[:len(line)-1]
					self.EntDict[Name]={}
				elif line==Lines[len(Lines)-1]:
					Key, Value = self.ParseLine(line[:len(line)])
					self.EntDict[Name][Key]=Value
					#shared.DPrint("YModConfigLoader",0,Name+": "+Key+"="+str(Value)+str(type(Value)))
				else:
					Key, Value = self.ParseLine(line[:len(line)-1])
					self.EntDict[Name][Key]=Value
					#shared.DPrint("YModConfigLoader",0,Name+": "+Key+"="+str(Value)+str(type(Value)))		

		return self.EntDict	

	def ParseLine(self,line):
		#DPrint("YModConfigLoader",1,"Parsing Line..")
		ComPar=split(line, "=")
		Key=ComPar[0]
		Value=ComPar[1]
		#Parsing Vector3:
		if Value[0]=="(" and Value[len(Value)-1]==")":
			Value=split(Value[1:len(Value)-1],",")
			#print Value
			Value=(float(Value[0]),float(Value[1]),float(Value[2]))

		#Parsing Lists:
		elif Value[0]=="[" and Value[len(Value)-1]=="]":
			Value=split(Value[1:len(Value)-1],",")
			print("Shit..")

		#Parsing Boolean:
		elif Value.lower()=="true":
			Value=True
		elif Value.lower()=="false":
			Value=False

		#Parsing None:
		elif Value.lower()=="none":
			Value=None

		#Parsing numbers
		else:
			#Parsing Integer
			try:
				Value=int(Value)
			except ValueError:
				pass

			#Parsing Float
			if type(Value)!=int:
				try:
					Value=float(Value)
				except ValueError:
					pass

		return Key, Value
