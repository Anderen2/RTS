#Hook (Shared Lib)
#An hook is something which can call functions based on events
#Better description @ http://maurits.tv/data/garrysmod/wiki/wiki.garrysmod.com/index64f4.html

from engine import shared, debug

class Hook():
	def __init__(self, creator):
		self.creator = creator
		self.grapplinghooks={}

	def new(self, hookname, args):
		self.grapplinghooks[hookname]={}
		self.grapplinghooks[hookname]["args"]=args
		self.grapplinghooks[hookname]["listeners"]=[]

	def call(self, hookname, *args):
		if hookname in self.grapplinghooks:
			for function in self.grapplinghooks[hookname]["listeners"]:
				ret = function(*args)
				if ret!=None:
					return ret
		else:
			shared.DPrint("Hook", 2, "Hook '"+hookname+"' does not exsist! Failed to call.")

	def Add(self, hookname, function):
		if hookname in self.grapplinghooks:
			if function not in self.grapplinghooks[hookname]["listeners"]:
				self.grapplinghooks[hookname]["listeners"].append(function)
			else:
				shared.DPrint("Hook", 2, "Function: '"+function.name+"' is already hooked to '"+hookname+"'!")
		else:
			shared.DPrint("Hook", 3, "Hook '"+hookname+"' does not exsist! Failed to add.")

	def RM(self, hookname, function):
		if hookname in self.grapplinghooks:
			if function in self.grapplinghooks[hookname]["listeners"]:
				self.grapplinghooks[hookname]["listeners"].remove(function)
			else:
				shared.DPrint("Hook", 2, "Cannot remove hook: Function: '"+function.name+"' not hooked to '"+hookname+"'!")

		else:
			shared.DPrint("Hook", 3, "Hook '"+hookname+"' does not exsist! Failed to remove.")