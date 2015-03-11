#Serverside Global-Action

from engine import shared, debug
from engine.World import posalgo, movetypes

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
			if self.targetunit:
				if shared.UnitManager.getIfActionPossible(self.unit, self.targetunit, True, False):
					if self.targetunit._health<1:
						self.unit._actionfinish()

					if self.fire == True:
						self.unit.PrimaryFire(self.targetunit)
				else:
					print("Action is not possible!")
					self.unit._actionfinish()
			else:
				print("Target Unit does not exsist!")
				self.unit._actionfinish()

	def pathEnd(self, lastpath):
		self.unit._sendActionState("close", self.unitpath)
		self.currentlyMoving=False
		self.unit._finishedmove()
		self.unit._vehicle.Hook.RM("OnPathEnd", self.pathEnd)

	def closeEnough(self):
		self.currentlyMoving = False
		self.unit._sendActionState("close", self.unitpath)
		self.unit._vehicle.clearPath()
		self.unit._finishedmove()
		self.unit._vehicle.Hook.RM("OnPathEnd", self.pathEnd)


	def tooFar(self, maxdist):
		"""Custom event provided by projectiles.py"""
		if not self.currentlyMoving:
			self.targetpos = self.targetunit.GetPosition()
			newpos = self.unit.GetPosition()

			#Get position close enough to target
			# maxdist = maxdist - 150 #Add a margin of 150 to make sure we are within range HARDCODE (Should be calculated according to A* Node space)
			# while True:
			# 	dist, newpos = movetypes.Move(newpos, self.targetpos, 5, 0)
			# 	print(str(dist)+"<"+str(maxdist))

			# 	if dist<maxdist:
			# 		break

			#Calculate A* Path from unit to newpos
			self.unitpath = shared.Pathfinder.aStarPath.Graph.Search2((self.unit._pos[0], self.unit._pos[2]), (self.targetpos[0], self.targetpos[2]))
			if self.unitpath == None:
				print("Impossible path requested by player!")
				return False

			self.currentlyMoving = maxdist
			# newpos = shared.Vector(newpos).net() #Optimalize the position for Networked usage
			self.unit._sendActionState("toofar", self.unitpath)
			self.unit._steerToPath(list(self.unitpath))
			self.unit._vehicle.Hook.Add("OnPathEnd", self.pathEnd)
			# self.unit._vehicle.Hook.Add("OnStep", self.onStep)