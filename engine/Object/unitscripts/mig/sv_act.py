#Serverside Opt Mig-Action

from engine import shared, debug
from time import time

class Action():
	actionid = "opt1"
	name = "Wait 5 secounds"
	description = "This action makes the unit wait 5 secounds before executing the next action"
	
	waypointType = None
	queueImage = "move"
	actguiPlacement = 1
	actguiImage = "move"

	abortable = True

	def __init__(self, unit, evt):
		self.data = evt
		self.unit = unit

		self.progress=0

		self.wait = 5
		self.timeleft = self.wait

	def begin(self):
		self.time = time()

	def abort(self):
		pass

	def finish(self):
		pass

	def update(self):
		self.timeleft = (time()-self.time)
		self.progress = (self.timeleft / self.wait)*100
		#print(self.progress)
		if self.timeleft>self.wait:
			self.unit._actionfinish()