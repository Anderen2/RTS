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
		debug.ACC("dircls", self.UnitDelAll, args=0, info="Clear/Delete all units directed by SimpleDir")

		self.gotoX=None
		self.gotoY=None
		self.gotoz=None

	def Action(self):
		self.Cast=[]
		self.CurrentSelection=[]
		self.UnitAdd("plane")
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
		self.Cast.append(shared.unitManager.CreateMov(4, 0, 0, name))

	def UnitDelAll(self):
		pass

	def evt_selected(self, selections):
		shared.DPrint("SimpleDir", 0, "Selections Updated")
		self.selections=selections
		self.CurrentSelection=[]
		for x in self.selections:
			unitID=int(split(x.getName(),"_")[1])
			self.CurrentSelection.append(shared.unitHandeler.Get(unitID))

	def evt_moveclick(self, pos):
		for x in self.CurrentSelection:
			x._setwaypoint(pos)
			shared.DPrint("SimpleDir", 0, "Moving unit: "+str(x))

	def evt_actionclick(self, pos):
		pass

	def Frame(self):
		#This will get executed each frame
		if self.Active:
			pass
			# if self.gotoX!=None:
			# 	x=self.gotoX
			# 	z=self.gotoZ
			# 	for actor in self.Cast:
			# 		print actor
			# 		print (x, z)
			# 		print (float(x), float(z))
			# 		dist=actor._movetowards(float(x), float(z))
			# 		if dist==0:
			# 			self.gotoX=None
			# 		print dist