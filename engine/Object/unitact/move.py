#UnitAction: Move group

from engine import shared, debug

class ActMove():
	def __init__(self, group, evt):
		self.waypointPos = evt["3dMouse"]
		self.waypointType = "Move"
		self.queueImage = "move"
		self.abortable = True
		self.aborted=False
		self.group = group

	def abort(self):
		shared.DPrint("UnitAction - Move", 0, "Action aborted!")
		self.aborted=True
		for unit in self.group.members:
			unit.nextwaypoint=None

	def begin(self):
		shared.DPrint("UnitAction - Move", 0, "Action begun!")
		for unit in self.group.members:
			unit._setwaypoint(self.waypointPos)

	def beginUnit(self, unit):
		shared.DPrint("UnitAction - Move", 0, "Action begun!")
		unit._setwaypoint(self.waypointPos)

	def update(self):
		if self.aborted==False:
			finished=True
			for unit in self.group.members:
				if unit.nextwaypoint!=None:
					finished=False

			if finished==True:
				self.group.actionFinished()