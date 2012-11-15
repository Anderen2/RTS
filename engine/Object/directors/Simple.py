#Director - Simple
#This is a simple director that allow you to test out unit animations and movement by using the console

from engine import shared, debug

class Director():
	def Init(self):
		debug.ACC("dirgo", self.UnitGo, args=3, info="Tell the units directed by SimpleDir to go towards the coordinates")
		debug.ACC("diraim", self.UnitAim, args=3, info="Tell the units directed by SimpleDir to aim towards the coordinates")
		debug.ACC("dirpri", self.UnitPri, args=0, info="Tell the units directed by SimpleDir to do the Primary Action")
		debug.ACC("dirsec", self.UnitPri, args=0, info="Tell the units directed by SimpleDir to do the Secondary Action")
		debug.ACC("diradd", self.UnitAdd, args=1, info="Add a unit under SimpleDir")
		debug.ACC("dircls", self.UnitDelAll, args=0, info="Clear/Delete all units directed by SimpleDir")

	def Action(self):
		self.Cast=[]
		self.UnitAdd("plane")

	def UnitGo(self, x, y, z):
		dist=2
		for x in xrange(10):
			for actor in self.Cast:
				print actor
				print (x, y, z)
				print (int(x), int(y), int(z))
				dist=actor._movetowards(int(x), int(y), int(z))
				print dist

	def UnitAim(self):
		pass

	def UnitPri(self):
		pass

	def UnitSec(self):
		pass

	def UnitAdd(self, name):
		self.Cast.append(shared.unitManager.CreateMov(4, 0, 0, "plane"))

	def UnitDelAll(self):
		pass