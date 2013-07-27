#Serverside Unitmanager
from traceback import print_exc
from importlib import import_module
from engine import shared, debug
from random import randrange
from engine.Object.unitscripts import sv_baseunit
import engine.World.pathfinding as pathfinding

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
		self.unitscripts["mig"] = import_module(modpath+"sv_mig").Unit
		
		#self.create("rawr", "mig", 10, (10, 10, 10))

	def req_build(self, name, x, y, z, Protocol=None):
		shared.DPrint(0, "netUnitManager", "Building "+str(name))

		## UNIT VALIDATION AND SERVERSIDE CREATION HERE

		player = shared.PlayerManager.getFromProto(Protocol)
		team = player.team
		userid = player.UID
		unitid = self.unitcount
		pos = (int(x), int(y), int(z))

		if self.create(player, name, unitid, pos):
			shared.PlayerManager.Broadcast(4, "build", [name, x, y, z, userid, unitid])
			self.unitcount+=1

		else:
			shared.DPrint(5, "netUnitManager", "Player: "+player.username+" tried to build an unit ("+str(name)+") but failed!")

	def massMove(self, unitlist, pos):
		amount=len(unitlist)
		shared.DPrint(0, "netUnitManager", "Massmoving "+str(amount)+ "units to "+str(pos))

		## PATHFINDING SPLITTING AND PATH VALIDATION HERE
		pickledunits=unitlist
		x, y, z = pos
		shared.PlayerManager.Broadcast(4, "massmove", [pickledunits, x, y, z])

	def create(self, owner, name, uid, pos):
		#NAME CHECK HERE
		if name in self.unitscripts:
			try:
				newunit=self.unitscripts[name](uid, owner, pos)
				owner.addUnit(newunit)
				return True

			except:
				shared.DPrint(0, "netUnitManager", "Unitscript for unit :"+str(name)+" has errors!")
				print_exc()
				return False

		else:
			shared.DPrint(0, "netUnitManager", "Unitscript for unit :"+str(name)+" does not exsist!")
			return False

	def getFromUID(self, uid, Player=None):
		if not Player:
			for player in shared.PlayerManager.PDict:
				for unit in shared.PlayerManager.PDict[player].Units:
					if unit.ID==uid:
						return unit

		if Player:
			print("PlayerUnits:"+str(Player.Units))
			for unit in Player.Units:
				if int(unit.ID)==int(uid):
					return unit

		return False