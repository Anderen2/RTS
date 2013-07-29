#Clientside Opt Mig-Action

from engine import shared, debug

class Action():
	actionid = "opt1"
	name = "Wait"
	description = "This action makes the unit wait 5 secounds before executing the next action"
	
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
		pass

	def update(self):
		pass