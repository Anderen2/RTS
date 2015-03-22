#shared.py
#This module is shared between all modules, and contains pointers to nessesary classes
from time import localtime
from math import sqrt, cos

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
MinimapManager=None

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
	def sum(self):
		return self.data[0]+self.data[1]
	def net(self):
		if len(self.data)==2:
			self.data = tuple([int(self.data[0]), int(self.data[1])])
			return self.data
		elif len(self.data)==3:
			self.data = tuple([int(self.data[0]), int(self.data[1]), int(self.data[2])])
			return self.data

class Vector3D():
	""" a stripped out class for 3D vectors"""
	
	__class__="Vector3D"

	def __init__(self, v=(0.,0.,0.)):
		self.V=tuple([v[i] for i in range(3)])

	def __getitem__(self,i):
		return self.V[i]
	
	def __mul__(self,s):
		"""Returns a Vector3D result of multiplication by scalar s"""
		
		return Vector3D(tuple([x*s for x in self.V]))
	def __div__(self,s):
		s = float(s)
		"""Returns a Vector3D result of multiplication by scalar s"""
		if not s==0 :
			return Vector3D([x/s for x in self.V])
		#ERROR DIVISION BY ZERO
		raise Exception("Error: Division by Zero!")
		return Vector3D.ZERO
	
	def __add__(self,A):
		return Vector3D(tuple([x1+x2 for (x1,x2) in zip(self.V,A)])) 
	
	def __sub__(self,A):
		return Vector3D(tuple([x1-x2 for (x1,x2) in zip(self.V,A)])) 

	def __cmp__(self,v):
		return cmp(self.V,v.asTuple())

	def __iter__(self):
		return self.V.__iter__()
	
	def __eq__(self,v):
		if (self.V==tuple(v)):
			return True
		return False
		
	def asTuple(self):
		return self.V

	def dotProduct2(self, b):
		return self.length() * b.length() * cos()
		
	def dotProduct(self, b):
		"""simple dot product function"""
		return sum([x1*x2 for (x1,x2) in zip(self.V,b)])
		#return sum([self.V[i]*b[i] for i in range(3)])
	
	def length(self):
		try:
			return sqrt(sum([x*x for x in self.V]))
		except ValueError:
			return 0
	
	def normalize(self):
		fLength =  self.length()
		if fLength > 1e-08 :
			fInvLength = 1.0 / fLength
			self.V=tuple([x*fInvLength for x in self.V])
			return fLength
		return 0

	def absolute(self):
		return Vector3D(abs(self.V)[0], abs(self.V)[1], abs(self.V)[2])
	
	def crossProduct(self,V):
		return Vector3D(tuple([self.V[1] * V[2] - self.V[2] * V[1],\
						self.V[2] * V[0] - self.V[0] * V[2],\
						self.V[0] * V[1] - self.V[1] * V[0]]))

	def truncate(self,A):
		i = 0
		NV = list(self.V)
		for x in self.V:
			if x>A:
				NV[i]=A
			elif x<-A:
				NV[i]=-A
			i+=1
		self.V = tuple(NV)

	def truncateActive(self, A):
		#Nonworking atm
		self.truncated = A
	
	def __str__(self):
		return "Vector3D"+str(self.V)

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