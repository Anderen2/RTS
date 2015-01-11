#Construct Structure Action
#Clientside Opt Action

from engine import shared, debug
from engine.Render import render3denteff

def generate(uid, desc=None, abort=True, placement=None):
	Unitmanager = shared.unitManager

	class BaseAction():
		actionid = uid
		name = Unitmanager.getUnit(uid).Name
		description = Unitmanager.getUnit(uid).Description
		
		waypointType = "Move"
		queueImage = Unitmanager.getUnit(uid).Image
		actguiPlacement = placement
		actguiImage = Unitmanager.getUnit(uid).Image

		abortable = True

		buildtime = Unitmanager.getUnit(uid).Buildtime
		cost = Unitmanager.getUnit(uid).Cost

		@classmethod
		def presend(cls, group, data, _type):
			if not "placement" in data:
				cls.PR_group = group
				cls.PR_data = data
				cls.PR_type = _type

				placement = render3denteff.PlacementEffect(shared.unitManager.getUnit(uid).BuildEntity, cls.presendPlaced)
				placement.Start()
				#None = presend is done, but no additional data is required to be sent
				#False = presend failed/action fails, so do not send action
				#True = presend is under progress, but cannot be sent at this time (Waiting for data)
				#All other = presend is done, and additional data returned needs to be sent with the action
				return True
			else:
				return None

		@classmethod
		def presendPlaced(cls, pos):
			print("Callback!")
			print(cls.PR_group)
			print(cls.PR_data)

			if cls.PR_type == "Do":
				cls.PR_group.requestActionDo(uid, {"placement":pos})
			elif cls.PR_type == "Now":
				cls.PR_group.requestActionNow(uid, {"placement":pos})
			elif cls.PR_type == "Add":
				cls.PR_group.requestActionAdd(uid, {"placement":pos})

		def __init__(self, unit, evt):
			self.evt = evt
			self.unit = unit

			self.data = evt
			self.progress=0

		def begin(self):
			pass
			#self.visualprogress = render3denteff.BuildEffect2(shared.unitManager.getUnit(uid).BuildEntity, self.evt["placement"])

		def abort(self):
			pass

		def finish(self):
			pass

		def update(self):
			pass

		def netupdate(self, state, data):
			if state=="toofar":
				self.unit._moveto(data)
			
	return BaseAction