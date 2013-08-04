#Serverside Global-Action

from engine import shared, debug
from engine.World import posalgo

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
		self.targetunit = shared.UnitManager.getFromUID(self.targetunitid)
		if self.targetunit:
			self.waypointPos = self.targetunit.GetPosition()
		else:
			self.unit._actionfinish()

		self.abortable = True
		self.progress=0
		self.aborted=None

	def begin(self):
		shared.DPrint("\tUnitAction - Move", 0, "Unit Action begun!")
		self.aborted=False
		self.unit.OnPrimaryAction(self.targetunit)
		self.fire=True

	def abort(self):
		shared.DPrint("\tUnitAction - Move", 0, "Unit Action aborted!")
		self.aborted=True
		self.unit.OnPrimaryActionAbort()
		self.fire=False
		
	def finish(self):
		self.unit.OnPrimaryActionFinish()
		self.fire=False

	def update(self):
		if self.targetunit:
			if self.targetunit._owner.team!=self.unit._owner.team:
				if shared.UnitManager.getIfActionPossible(self.unit, self.targetunit, True, True):
					if self.targetunit._health<1:
						self.unit._actionfinish()

					if self.fire == True:
						self.unit.PrimaryFire(self.targetunit)
				else:
					self.unit._actionfinish()