#Serverside Global-Action

from engine import shared, debug

class Action():
	actionid = "pri"
	name = "Move unit"
	description = "This action moves units to a different position"

	waypointType = "Move"
	queueImage = "move"
	actguiPlacement = False
	actguiImage = "move"

	abortable = True

	@classmethod
	def presend(cls, group, data, _type):
		if not "path" in data:
			cls.PR_group = group
			cls.PR_data = data
			cls.PR_type = _type

			centerPos = group.getCenterPosition()
			targetPos = data["3dMouse"]

			path = shared.Pathfinder.aStarPath.Graph.Search2((centerPos[0], centerPos[2]), (targetPos[0], targetPos[2]))
			if path == None:
				print("Impossible path requested by player!")
				return False
				
			#None = presend is done, but no additional data is required to be sent
			#False = presend failed/action fails, so do not send action
			#True = presend is under progress, but cannot be sent at this time (Waiting for data)
			#All other = presend is done, and additional data returned needs to be sent with the action
			print "PRESEND _____________________"
			print path
			return {"path":path}
		else:
			return None

	def __init__(self, unit, data):
		print("Data")
		self.data = data
		print("INIT ______________________________")
		print("Path")
		self.path = list(data["path"]) #Note to self: Try to remember that a = b creates an reference to b, not an copy. This will save you plenty of time debugging all the time
		print data

		print("abort")
		self.abortable = True

		print("progress")
		self.progress=0
		self.aborted=None
		self.unit = unit


	def begin(self):
		shared.DPrint("UnitAction - Move", 0, "Action begun!")
		self.aborted=False
		firstpoint = self.path.pop(0)

		self.unit._steerto(firstpoint)

	def abort(self):
		shared.DPrint("UnitAction - Move", 0, "Action aborted!")
		self.aborted=True
		self.unit._stopmove()
		
	def finish(self):
		pass

	def update(self):
		if self.aborted==False:
			if self.unit._movetopoint==None:
				if len(self.path)!=0:
					nextpoint = self.path.pop(0)
					self.unit._steerto(nextpoint)