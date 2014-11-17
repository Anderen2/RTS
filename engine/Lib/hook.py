#Hook (Shared Lib)
#An hook is something which can call functions based on events
#Better description @ http://maurits.tv/data/garrysmod/wiki/wiki.garrysmod.com/index64f4.html

from engine import shared, debug
from time import time
from operator import itemgetter

class Hook():
	def __init__(self, creator):
		self.creator = creator
		self.grapplinghooks={}
		self.ALLPROFILING = True
		shared.Profile = []


	def new(self, hookname, args):
		self.grapplinghooks[hookname]={}
		self.grapplinghooks[hookname]["args"]=args
		self.grapplinghooks[hookname]["listeners"]=[]

	def call(self, hookname, *args):
		if self.ALLPROFILING:
			ret = self.callProfiler(hookname, *args)
			return ret
		if hookname in self.grapplinghooks:
			for function in self.grapplinghooks[hookname]["listeners"]:
				ret = function(*args)
				if ret!=None:
					return ret
		else:
			shared.DPrint("Hook", 2, "Hook '"+hookname+"' does not exsist! Failed to call.")

	def callProfiler(self, hookname, *args):
		if hookname in self.grapplinghooks:
			profile = {}
			for function in self.grapplinghooks[hookname]["listeners"]:
				profile[str(function)] = {}
				profile[str(function)]["start"] = time()
				ret = function(*args)
				profile[str(function)]["end"] = time()
				self.printNiceProfile(profile)
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

	def removeAll(self):
		for hook in self.grapplinghooks:
			self.grapplinghooks[hook]["listeners"] = []
		print self.grapplinghooks

	def printNiceProfile(self, hookprofile):
		sortlist = []
		if type(hookprofile) != bool:
			for function, profile in hookprofile.iteritems():
				timeused = profile["end"] - profile["start"]
				sortlist.append((function, timeused))
			#sorted(sortlist, key=itemgetter(1))

			#for value in sortlist:
			#	print ("%s: %f" % value)
			#return sortlist

			appendlist = sortlist[:]
			for pro_value in shared.Profile:
				valueExists = False
				for list_value in sortlist:
					if pro_value[0] == list_value[0]:
						valueExists = (pro_value, list_value)

				if valueExists:
					indx = shared.Profile.index(valueExists[0])
					shared.Profile[indx] = valueExists[1]
					appendlist.remove(valueExists[1])

			shared.Profile.extend(appendlist)

def showProfile():
	shared.Profile = sorted(shared.Profile, key=itemgetter(1))
	retstr = "Top usage (reverse order):"
	for value in shared.Profile:
		retstr = retstr + "\n--\n" + "%s: %f" % value

	print retstr
	return retstr

debug.ACC("profile", showProfile, "Show profiler times", 0)