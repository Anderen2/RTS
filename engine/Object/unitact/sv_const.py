#Unit under construction action
#Serverside Global-Action

from engine import shared, debug

class Action():
	actionid = "const"
	name = "Construction"
	description = "This unit is under construction.."

	waypointType = None
	queueImage = None
	actguiPlacement = False
	actguiImage = "construction"

	abortable = False

	def __init__(self, unit, evt):
		self.data = evt
		self.waypointPos = None

		self.abortable = False

		self.progress=0
		self.aborted=None
		self.unit = unit


	def begin(self):
		self.oldacts = self.unit.Actions
		self.unit.Actions = []

	def abort(self):
		self.unit._hackishDie()
		
	def finish(self):
		self.unit.Actions = self.oldacts

	def update(self):
		pass