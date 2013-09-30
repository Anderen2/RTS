#Unit under construction action
#Client Global-Action

from engine import shared, debug
from engine.Render import render3denteff
from time import time

class Action():
	actionid = "const"
	name = "Construction"
	description = "This unit is under construction.."

	waypointType = None
	queueImage = None
	actguiPlacement = False
	actguiImage = "construction"

	abortable = False

	def __init__(self, unit, evt):
		self.data = evt
		self.waypointPos = None

		self.abortable = False

		self.progress=0
		self.aborted=None
		self.unit = unit
		self.buildtime = unit.Buildtime

	def begin(self):
		self.oldacts = self.unit.Actions
		self.unit.Actions = []
		self.unit._group.getAllCommonActions()
		self.unit._group.updateSelectedVisuals()

		self.time = time()
		self.buildeffect = render3denteff.BuildEffect(self.unit.GetEntity())
		self.buildeffect.Start()

	def abort(self):
		self.buildeffect.Remove()
		self.buildeffect = None
		self.unit._die()
		
	def finish(self):
		self.unit.Actions = self.oldacts
		self.unit._group.getAllCommonActions()
		self.unit._group.updateSelectedVisuals()

		self.buildeffect.Remove()
		self.buildeffect = None

	def update(self):
		self.timeleft = (time()-self.time)
		self.progress = (self.timeleft / self.buildtime)*100
		self.buildeffect.UpdateProgress(self.progress)