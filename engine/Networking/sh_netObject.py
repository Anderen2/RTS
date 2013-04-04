#ObjectManager
from traceback import print_exc
from engine import shared, debug

class ObjectManager():
	def __init__(self):
		self.olist={}
		shared.objectManager=self

	def addEntry(self, otype, ID, obj):
		self.olist[otype+ID]=obj

	def runMethod(self, prot, obj, method, arg):
		try:
			if arg!=None:
				ret=getattr(self.olist[obj], method)(Protocol=prot, *arg)
				if ret!=None:
					prot.sendMethod(0, method, ret)
			else:
				ret=getattr(self.olist[obj], method)(Protocol=prot)
				if ret!=None:
					prot.sendMethod(0, method, ret)

		except KeyError:
			try:
				print(self.olist[obj])
				return 1
			except:
				print("Invalid object: "+str(obj))
				print_exc()
				return 3

		except AttributeError:
			if obj in self.olist:
				print("Invalid method: "+str(obj)+"."+method)
				print_exc()
				return 2
			else:
				print_exc()
				return 1
		except:
			print_exc()
			return 1

	def getVarible(self, obj, var):
		try:
			return getattr(self.olist[obj], var)

		except KeyError:
			try:
				print(self.olist[obj])
				return 1
			except:
				print("Invalid object")
				return 3

		except:
			print_exc()
			return 1

	def setVarible(self, obj, var, new):
		try:
			setattr(self.olist[obj], var, new)
			return 0

		except KeyError:
			try:
				print(self.olist[obj])
				return 1
			except:
				print("Invalid object")
				return 3

		except:
			print_exc()
			return 1

	def getEntryByClass(self, name):
		for x in self.olist:
			if self.olist[x].__class__.__name__==name:
				return x
		return 1

	def getEntryByName(self, name):
		for x in self.olist:
			try:
				if self.olist[x].name==name:
					return x
			except:
				pass
		return 1

	def getEntryByID(self, ID):
		for x in self.olist:
			try:
				if self.olist[x].ID==ID:
					return x
			except:
				pass
		return 1