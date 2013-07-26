#Serverside Mig-Action

from engine import shared, debug

class Action():
	actionid = "move"
	name = "Move unit"
	description = "This action moves units to a different position"

	def __init__(self, unit, evt):
		self.data = evt
		self.waypointPos = evt["3dMouse"]
		self.waypointType = "Move"
		self.queueImage = "move"
		self.actguiPlacement = False
		self.actguiImage = "move"

		self.abortable = True

		self.progress=0
		self.aborted=False
		self.unit = unit

	def abort(self):
		shared.DPrint("UnitAction - Act1", 0, "Action aborted!")
		self.aborted=True
		self.unit._stopmove()

	def begin(self):
		shared.DPrint("UnitAction - Move", 0, "Action begun!")
		self.unit._moveto(self.data["pos"])

	def update(self):
		if self.aborted==False:
			# finished=True
			# for unit in self.group.members:
			# 	if unit.nextwaypoint!=None:
			# 		finished=False

			# if finished==True:
			# 	self.group.actionFinished()
			pass