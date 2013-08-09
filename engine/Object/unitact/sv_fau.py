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
		self.currentlyMoving = False

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
		if not self.aborted:
			if not self.currentlyMoving:
				if self.targetunit:
					if shared.UnitManager.getIfActionPossible(self.unit, self.targetunit, True, False):
						if self.targetunit._health<1:
							self.unit._actionfinish()

						if self.fire == True:
							self.unit.PrimaryFire(self.targetunit)
					else:
						self.unit._actionfinish()
				else:
						self.unit._actionfinish()
			else:
				if self.unit._movetopoint==None:
					print("Done!")
					self.currentlyMoving=False

	def tooFar(self, dist):
		"""Custom event provided by projectiles.py"""
		if not self.currentlyMoving:
			foo = True
			self.waypointPos = self.targetunit.GetPosition()
			newpos = self.unit._pos
			while foo:
				simdist, newpos = self.unit._simulateMoveStep((self.waypointPos[0], self.waypointPos[2]), 2, src=(newpos[0], newpos[2]))
				print(str(simdist)+"<"+str(dist))
				if (simdist)<dist:
					foo = False

			self.currentlyMoving = True
			self.unit._sendActionState("toofar", newpos)
			self.unit._moveto(newpos)