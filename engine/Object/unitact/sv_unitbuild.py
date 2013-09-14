#Build Unit Action
#Serverside Opt Action

from engine import shared, debug
from time import time

def generate(uid, desc=None, abortable=True, placement=None):
	Unitmanager = shared.UnitManager

	class BaseAction():
		actionid = uid
		name = Unitmanager.getUnit(uid).Name
		description = Unitmanager.getUnit(uid).Description
		
		waypointType = "Move"
		queueImage = Unitmanager.getUnit(uid).Image
		actguiPlacement = placement
		actguiImage = Unitmanager.getUnit(uid).Image

		abortable = True

		buildtime = Unitmanager.getUnit(uid).Buildtime
		cost = Unitmanager.getUnit(uid).Cost

		def __init__(self, unit, evt):
			self.evt = evt
			self.unit = unit

			print(self.unit.Destination)
			if self.unit.Destination!=None:
				if type(self.unit.Destination)==tuple:
					self.waypointPos = self.unit.Destination
					print(self.waypointPos)
				else:
					self.waypointPos = self.unit.Destination._pos

			self.data = {"3dMouse":self.waypointPos}

			self.progress=0

			self.timeleft = self.buildtime

		def begin(self):
			self.time = time()

		def abort(self):
			pass

		def finish(self):
			pass

		def update(self):
			self.timeleft = (time()-self.time)
			self.progress = (self.timeleft / self.buildtime)*100
			#print(self.progress)
			if self.timeleft>self.buildtime:
				shared.UnitManager.build(self.actionid, self.unit._owner, self.unit._pos, "pri", {"3dMouse":self.waypointPos})
				self.unit._actionfinish()
	
	return BaseAction