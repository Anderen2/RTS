#Build an MIG Action
#Serverside Opt Action

from engine import shared, debug

def generate(uid, desc=None, abort=True, placement=None):
	Unitmanager = shared.unitManager

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
				else:
					self.waypointPos = self.unit.Destination._pos

			self.data = {"waypoint":self.waypointPos}

			self.progress=0

		def begin(self):
			pass

		def abort(self):
			pass

		def finish(self):
			pass

		def update(self):
			pass
			
	return BaseAction