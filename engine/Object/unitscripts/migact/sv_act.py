#Serverside Mig-Action

from engine import shared, debug

class Action():
	def __init__(self, unit, evt):
		self.actionid = "example"
		self.name = "Example Action"
		self.description = "This action does examples"
		self.waypointPos = evt["3dMouse"]
		self.waypointType = "Move"
		self.queueImage = "move"
		self.actguiPlacement = 1
		self.actguiImage = "move"

		self.abortable = True

		self.progress=0
		self.aborted=False
		self.unit = unit

	def abort(self):
		shared.DPrint("UnitAction - Act1", 0, "Action aborted!")
		self.aborted=True

	def begin(self):
		shared.DPrint("UnitAction - Move", 0, "Action begun!")

	def update(self):
		if self.aborted==False:
			finished=True
			for unit in self.group.members:
				if unit.nextwaypoint!=None:
					finished=False

			if finished==True:
				self.group.actionFinished()