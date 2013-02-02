#ObjectManager
class ObjectManager():
	def __init__(self):
		self.olist={}

	def addEntry(self, otype, ID, obj):
		self.olist[otype+ID]=obj

	def runMethod(self, obj, method, arg):
		try:
			getattr(self.olist[obj], method)(*arg)
			return 0

		except KeyError:
			try:
				print(self.olist[obj])
				return 1
			except:
				print("Invalid object")
				return 3

		except AttributeError:
			if obj in self.olist:
				print("Invalid method")
				return 2
			else:
				print_exc()
				return 1
		except:
				print_exc()
				return 1