#Director - Simple
#This is a simple director that allow you to test out unit animations and movement by using the console

from engine import shared, debug
from string import split

class Director():
	def __init__(self):
		self.Active=False

	def Init(self):
		#debug.ACC("dirgo", self.UnitGo, args=2, info="Tell the units directed by SimpleDir to go towards the coordinates")
		debug.ACC("dirbuild", self.UnitBuild, args=1, info="Simulate a unit build on the server")

	def Action(self):
		self.Cast=[]
		self.CurrentSelection=[]
		self.Active=True

	def UnitBuild(self, name):
		pass
		#self.Cast.append(shared.unitManager.Create(0, name))

	def evt_selected(self, selections):
		shared.DPrint("SimpleDir", 0, "Selections Updated")
		self.selections=selections
		self.CurrentSelection=[]
		for x in self.selections:
			unitID=int(split(x.getName(),"_")[1])
			self.CurrentSelection.append(shared.unitHandeler.Get(unitID))

	def evt_moveclick(self, pos):
		for x in self.CurrentSelection:
			#x._setwaypoint(pos)
			shared.DPrint("SimpleDir", 0, "Moving unit: "+str(x))

	def evt_actionclick(self, data):
		for x in self.CurrentSelection:
			pass
			#x.entity.node.showBoundingBox(True)
			#shared.reactor.callLater(1, lambda: x.entity.node.showBoundingBox(False))

	def Frame(self):
		#This will get executed each frame
		if self.Active:
			pass