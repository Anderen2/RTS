#shared.py
#This module is shared between all modules, and contains pointers to nessesary classes
from time import localtime

wd="./" #Workingdirectory
side=None
#Its not nessesary to declare all these as none before declaring them to what they are. But it gives a quick overview over what the names are
render=None

renderRoot=None

render3dScene=None
render3dCamera=None
render3dSelectStuff=None

renderGUI=None

renderioInput=None

renderphysPhys=None

unitManager=None
unitHandeler=unitManager #Dirty Lazy Temporary Shitty Bad Workaround (Switched name, Manager sounded better)
propManager=None
zoneManager=None
DirectorManager=None

decHandeler=None

EntityHandeler=None

console=None

ParseCommand=None

LogFile=None

#Additional Types
class Vector( object ):
	def __init__(self, *data):
		if type(data[0])==tuple:
			self.data = data[0]
		elif type(data[0])==list:
			self.data = tuple(data[0])
		else:
			self.data = data

		if len(self.data)>2:
			self.x = self.data[0]
			self.y = self.data[1]
			self.z = self.data[2]
		elif len(self.data)==2:
			self.x = self.data[0]
			self.y = self.data[1]
			
	def __repr__(self):
		return repr(self.data) 
	def __add__(self, other):
		return tuple( (a+b for a,b in zip(self.data, other.data) ) )  
	def __sub__(self, other):
		return tuple( (float(float(a)-float(b)) for a,b in zip(self.data, other.data) ) )
	def __mul__(self, other):
		return tuple( (a*b for a,b in zip(self.data, other.data) ) )
	def __div__(self, other):
		return tuple( (a/b for a,b in zip(self.data, other.data) ) )

def logInit(name):
	global LogFile
	try:
		try:
			Log2=open("logs/"+name+".log2", "r")
			Log3=open("logs/"+name+".log3", "w")
			Log3.write(Log2.read(100))
			Log3.close()
			Log2.close()
		except:
			pass

		try:
			Log1=open("logs/"+name+".log1", "r")
			Log2=open("logs/"+name+".log2", "w")
			Log2.write(Log1.read(100))
			Log2.close()
			Log1.close()
		except:
			pass

		try:
			Log=open("logs/"+name+".log", "r")
			Log1=open("logs/"+name+".log1", "w")
			Log1.write(Log.read(100))
			Log1.close()
			Log.close()
		except:
			pass

		LogFile=open("logs/"+name+".log", "w")
	except:
		print("Failed creating logfile")

LogSep="z_*"
TimeSep="|"
def DPrint(From, Warnlvl, Str):
	global LogFile
	#Debugprint, this function simplifies reading from the console + logging
	#From = Numerical Index which says what the print is from ["main", "render", "render3d", "rendergui", "renderio", "renderphys", "unit"]
	#Warnlvl = Numerical Index which says what warnlevel it is 0=Debugging, 1=Info > 5=Critical
	foo=str(localtime()[3])
	bar=str(localtime()[4])
	fob=str(localtime()[5])
	req=foo+TimeSep+bar+TimeSep+fob
	preq="0"*(2-len(foo))+foo+":"+"0"*(2-len(bar))+bar+":"+"0"*(2-len(fob))+fob+" "
	# try:
	LogFile.write(req+LogSep+str(From)+LogSep+str(Warnlvl)+LogSep+str(Str)+"\n")
	LogFile.flush()
	# except:
	# 	print("Failed writing to log")
	print(preq+str(Str))