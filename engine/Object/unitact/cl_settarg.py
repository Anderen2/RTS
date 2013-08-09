#Building defaultaction: Set waypoint
#Clientside Global-Action

from engine import shared, debug

class Action():
	actionid = "pri"
	name = "Set Unit Waypoint"
	description = "This action sets default waypoint for new units"

	waypointType = None
	queueImage = None
	actguiPlacement = False
	actguiImage = "move"

	abortable = False

	def __init__(self, unit, evt):
		self.data = evt
		self.targetunitid = evt["unitid"]
		self.targetunit = shared.netUnitManager.getFromUID(self.targetunitid)

		self.abortable = True

		self.progress=0
		self.aborted=None
		self.unit = unit


	def begin(self):
		shared.DPrint("UnitAction - Move", 0, "Action begun!")
		self.aborted=False
		self.unit.Destination = self.targetunit
		
	def abort(self):
		pass
		
	def finish(self):
		pass

	def update(self):
		pass