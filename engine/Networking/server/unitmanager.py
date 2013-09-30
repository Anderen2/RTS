#Serverside Unitmanager
from traceback import print_exc
from importlib import import_module
from engine import shared, debug
from random import randrange
from engine.Object.unitscripts import sv_baseunit
import engine.World.pathfinding as pathfinding
from engine.World import posalgo

class UnitManager():
	def __init__(self):
		shared.UnitManager=self
		shared.objectManager.addEntry(0,4, self)

		self.unitcount=0

		self.unitscripts={}
		self.Load()

		#Pathfinding
		shared.Pathfinder = pathfinding

	def Load(self):
		#Find and import all availible UnitScripts HERE
		modpath = "engine.Object.unitscripts."
		self.unitscripts["mig"] = import_module(modpath+"mig.sv_mig").Unit
		self.unitscripts["build"] = import_module(modpath+"build.sv_build").Unit
		self.unitscripts["tank"] = import_module(modpath+"tank.sv_tank").Unit
		self.unitscripts["robot"] = import_module(modpath+"robot.sv_robot").Unit

	def req_build(self, name, x, y, z, Protocol=None):
		shared.DPrint(0, "netUnitManager", "Building "+str(name))

		player = shared.PlayerManager.getFromProto(Protocol)
		pos = (int(x), int(y), int(z))

		self.build(name, player, pos)

	def build(self, name, player, pos, act=None, data=None):
		team = player.team
		userid = player.UID
		unitid = self.unitcount
		newunit = self.create(player, name, unitid, pos)
		if newunit:
			attribs = newunit.pendingattrib.copy()
			newunit.pendingattrib = {}
			shared.PlayerManager.Broadcast(4, "build", [name, userid, unitid, attribs])
			self.unitcount+=1

			if act!=None:
				newgroup = shared.GroupManager.createGroup(False, [newunit], player)
				action = newgroup.getActionByID(act)
				newgroup.doAction(action, data)
				return newunit, newgroup

			return newunit

		else:
			shared.DPrint(5, "netUnitManager", "Player: "+player.username+" tried to build an unit ("+str(name)+") but failed!")


	def create(self, owner, name, uid, pos):
		if name in self.unitscripts:
			try:
				#shared.Gamemode._playerReqUnit(owner, self.unitscripts[name])
				newunit=self.unitscripts[name](uid, owner, pos)
				owner.addUnit(newunit)
				return newunit

			except:
				shared.DPrint(0, "netUnitManager", "Unitscript for unit :"+str(name)+" has errors!")
				print_exc()
				return False

		else:
			shared.DPrint(0, "netUnitManager", "Unitscript for unit :"+str(name)+" does not exsist!")
			return False

	### UnitGetters

	def getUnit(self, UnitID):
		if UnitID in self.unitscripts:
			return self.unitscripts[UnitID]
		else:
			return None

	def generateAllUnits(self, Player=None):
		if not Player:
			for player in shared.PlayerManager.PDict:
				for unit in shared.PlayerManager.PDict[player].Units:
					yield unit

		elif Player:
			for unit in Player.Units:
				yield unit

	def getFromUID(self, uid, Player=None):
		for unit in self.generateAllUnits(Player):
			if unit.ID==uid:
				return unit

		return False

	def getUnitAtPos(self, position, exact=False):
		if len(position)==2: #2D Matching
			if exact==False:
				position=(int(position[0]), int(position[1]))

			for unit in self.generateAllUnits(None):
				if exact==False:
					if int(unit._pos[0]) == position[0]:
						if int(unit._pos[2]) == position[1]:
							return unit
				else:
					if unit._pos[0] == position[0]:
						if unit._pos[2] == position[1]:
							return unit

		if len(position)==3: #3D Matching
			if exact==False:
				position=(int(position[0]), int(position[1]), int(position[2]))
			for unit in self.generateAllUnits(None):
				if exact==False:
					if int(unit._pos[0]) == position[0]:
						if int(unit._pos[1]) == position[1]:
							if int(unit._pos[2]) == position[2]:
								return unit
				else:
					if unit._pos[0] == position[0]:
						if unit._pos[1] == position[1]:
							if unit._pos[2] == position[2]:
								return unit

	def generateUnitsWithin(self, square):
		for unit in self.generateAllUnits(None):
			if unit._pos[0] < square[0][0]: #Top X
				if unit._pos[0] > square[1][0]: #Bottom X
					if unit._pos[2] < square[0][1]: #Top Y
						if unit._pos[2] > square[1][1]: #Bottom Y
							yield unit

	### UnitCheckers
	def getIfActionPossible(self, unit, targetunit, damaging, view):
		FRIENDLYFIRE = True
		if unit._health>0:
			if damaging:
				if unit._owner.team!=targetunit._owner.team or FRIENDLYFIRE:
					if not view or posalgo.in_circle(unit._pos[0], unit._pos[2], unit._viewrange, targetunit._pos[0], targetunit._pos[2]):
						return True
			else:
				if not view or posalgo.in_circle(unit._pos[0], unit._pos[2], unit._viewrange, targetunit._pos[0], targetunit._pos[2]):
					return True

		return False