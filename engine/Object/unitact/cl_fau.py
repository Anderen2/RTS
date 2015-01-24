#Clientside Global-Action

from engine import shared, debug

class Action():
	actionid = "fau"
	name = "Fire at unit"
	description = "This action fires at an unit"
	
	waypointType = "Move"
	queueImage = "move"
	actguiPlacement = False
	actguiImage = "move"

	abortable = True

	def __init__(self, unit, evt):
		self.data = evt
		self.unit = unit

		self.targetunitid = evt["unitid"]
		self.targetunit = shared.netUnitManager.getFromUID(self.targetunitid)
		if self.targetunit:
			self.waypointPos = self.targetunit.GetPosition()
			print("\n\n\n waypointPos")
			print(self.waypointPos)
			print("\n\n\n")

		self.abortable = True
		self.progress=0
		self.aborted=None


	def begin(self):
		shared.DPrint("UnitAction - Move", 0, "Action begun!")
		self.aborted=False
		if not self.targetunit.getAttribute("unit.health")<1:
			self.unit.AimAtUnit(self.targetunit)
		self.unit.OnPrimaryAction(self.targetunit)

	def abort(self):
		shared.DPrint("UnitAction - Act1", 0, "Action aborted!")
		self.aborted=True
		self.unit.OnPrimaryActionAbort()

	def finish(self):
		self.unit.OnPrimaryActionFinish()

	def update(self):
		if self.aborted==False and self.targetunit._isAlive:
			self.unit.AimAtUnit(self.targetunit)

	def netupdate(self, state, data):
		if state=="toofar":
			self.unit._moveto(data)