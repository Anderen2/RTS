#Construct Structure Action
#Serverside Opt Action

from engine import shared, debug
from time import time

def generate(uid, desc=None, abortable=True, placement=None):
	Unitmanager = shared.UnitManager

	class BaseAction():
		actionid = uid
		name = Unitmanager.getUnit(uid).Name
		description = Unitmanager.getUnit(uid).Description
		
		waypointType = None
		queueImage = Unitmanager.getUnit(uid).Image
		actguiPlacement = placement
		actguiImage = Unitmanager.getUnit(uid).Image

		abortable = True

		buildtime = Unitmanager.getUnit(uid).Buildtime
		cost = Unitmanager.getUnit(uid).Cost

		def __init__(self, unit, evt):
			self.evt = evt
			self.unit = unit

			self.progress=0

			self.timeleft = self.buildtime
			print(self.evt["placement"])

		def begin(self):
			self.constructionunit, self.constructiongroup = shared.UnitManager.build(self.actionid, self.unit._owner, self.evt["placement"], "const", {})
			self.time = time()

		def abort(self):
			self.constructiongroup.abortCurrentAction()

		def finish(self):
			pass

		def update(self):
			self.timeleft = (time()-self.time)
			self.progress = (self.timeleft / self.buildtime)*100
			#print(self.progress)
			if self.timeleft>self.buildtime:
				self.constructionDone()

		def constructionDone(self):
			self.unit._actionfinish()
			self.constructionunit._actionfinish()
	
	return BaseAction