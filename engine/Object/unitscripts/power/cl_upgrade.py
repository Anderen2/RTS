#Clientside Opt Mig-Action

from engine import shared, debug

class Action():
	actionid = "pwr_upgrade"
	name = "Upgrade"
	description = "Upgrade reactor to output 100% more power"
	
	waypointType = None
	queueImage = "move"
	actguiPlacement = 0
	actguiImage = "move"

	abortable = True

	def __init__(self, unit, evt):
		self.data = evt
		self.unit = unit

		self.progress=0

	def begin(self):
		pass

	def abort(self):
		pass

	def finish(self):
		self.unit._entity.setIllumination(1,0,0)
		pass

	def update(self):
		pass