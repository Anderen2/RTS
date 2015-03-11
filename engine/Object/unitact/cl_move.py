#Clientside Global-Action

from engine import shared, debug

class Action():
	actionid = "pri"
	name = "Move unit"
	description = "This action moves units to a different position"
	
	waypointType = "Move"
	queueImage = "move"
	actguiPlacement = False
	actguiImage = "move"

	def __init__(self, unit, data):
		self.data = data
		self.waypointPos = data["3dMouse"]
		self.path = data["path"][unit.ID]

		self.abortable = True

		self.progress=0
		self.aborted=None
		self.unit = unit


	def begin(self):
		shared.DPrint("UnitAction - Move", 0, "Action begun!")
		self.aborted=False

		self.unit._steerToPath(list(self.path))
	
	def abort(self):
		shared.DPrint("UnitAction - Act1", 0, "Action aborted!")
		self.aborted=True
		self.unit._stopmove()

	def finish(self):
		print("\nI should have stopped here!")
		self.unit._finishedmove()
		self.unit._setPosition((self.data["path"][self.unit.ID][-1][0], self.unit.GetPosition()[1], self.data["path"][self.unit.ID][-1][1]))

	def update(self):
		# if self.aborted==False:
		# 	if self.unit._movetopoint==None:
		# 		if self.unit._movetype == -99: #MOVETYPE_AIR
		# 			self.unit._steerto(self.data["3dMouse"])
		# 		else:
		# 			if len(self.path)!=0:
		# 				nextpoint = self.path.pop(0)
		# 				self.unit._steerto(nextpoint)
		pass