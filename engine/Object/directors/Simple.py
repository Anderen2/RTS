#Director - Simple
#This is a simple director that allow you to test out unit animations and movement by using the console

from engine import shared, debug
from string import split

class Director():
	def __init__(self):
		self.Active=False

	def Init(self):
		debug.ACC("dirgo", self.UnitGo, args=2, info="Tell the units directed by SimpleDir to go towards the coordinates")
		debug.ACC("diraim", self.UnitAim, args=3, info="Tell the units directed by SimpleDir to aim towards the coordinates")
		debug.ACC("dirpri", self.UnitPri, args=0, info="Tell the units directed by SimpleDir to do the Primary Action")
		debug.ACC("dirsec", self.UnitPri, args=0, info="Tell the units directed by SimpleDir to do the Secondary Action")
		debug.ACC("diradd", self.UnitAdd, args=1, info="Add a unit under SimpleDir")
		debug.ACC("diradde", self.UnitAddEnemy, args=1, info="Add a unit under SimpleDir")
		debug.ACC("dircls", self.UnitDelAll, args=0, info="Clear/Delete all units directed by SimpleDir")

		self.gotoX=None
		self.gotoY=None
		self.gotoz=None

	def Action(self):
		self.Cast=[]
		self.CurrentSelection=[]
		#self.UnitAdd("plane")
		self.Active=True

	def UnitGo(self, x, z):
		self.gotoX=x
		self.gotoZ=z

	def UnitAim(self, x, y, z):
		for actor in self.Cast:
			actor._look(x, y, z)

	def UnitPri(self):
		pass

	def UnitSec(self):
		pass

	def UnitAdd(self, name):
		unit=shared.unitManager.Create(0, name)
		self.Cast.append(unit)
		shared.FowManager.addAlly(unit.entity.node, 500)

		shared.FowManager.nodeUpdate(unit.entity.node)
		#print(shared.FowManager.getState(unit.entity.node))

	def UnitAddEnemy(self, name):
		unit=shared.unitManager.Create(0, name)
		self.Cast.append(unit)
		shared.FowManager.addEnemy(unit.entity.node)

		shared.FowManager.nodeUpdate(unit.entity.node)
		#print(shared.FowManager.getState(unit.entity.node))

	def UnitDelAll(self):
		pass

	def evt_selected(self, selections):
		shared.DPrint("SimpleDir", 0, "Selections Updated")
		self.selections=selections
		
		for x in self.CurrentSelection:
			x._deselected()

		self.CurrentSelection=[]

		for x in self.selections:
			unitID=int(split(x.getName(),"_")[1])
			unit=shared.unitHandeler.Get(unitID)
			unit._selected()
			self.CurrentSelection.append(unit)

	def evt_moveclick(self, pos):
		for x in self.CurrentSelection:
			x._setwaypoint(pos)
			shared.DPrint("SimpleDir", 0, "Moving unit: "+str(x))

	def evt_actionclick(self, data):
		for x in self.CurrentSelection:
			x.entity.node.showBoundingBox(True)
			shared.reactor.callLater(1, lambda: x.entity.node.showBoundingBox(False))

	def Frame(self):
		#This will get executed each frame
		if self.Active:
			pass