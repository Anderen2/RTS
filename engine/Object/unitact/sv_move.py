#Serverside Global-Action

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
		self.aborted=None
		self.unit = unit

	def abort(self):
		shared.DPrint("UnitAction - Move", 0, "Action aborted!")
		self.aborted=True
		self.unit._stopmove()

	def begin(self):
		shared.DPrint("UnitAction - Move", 0, "Action begun!")
		self.aborted=False
		self.unit._moveto(self.data["3dMouse"])

	def update(self):
		if self.aborted==False:
			if self.unit._movetopoint==None:
				self.unit._actionfinish()