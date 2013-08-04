#Clientside Unitmanager
from importlib import import_module
from engine import shared, debug
from engine.Object.unitscripts import cl_baseunit

class UnitManager():
	def __init__(self):
		shared.netUnitManager=self
		shared.objectManager.addEntry(0,4, self)

		#self.unitregister={}
		self.unitscripts={}
		self.Load()

	def Load(self):
		#Find and import all availible UnitScripts HERE
		modpath = "engine.Object.unitscripts."
		self.unitscripts["mig"] = import_module(modpath+"cl_mig").Unit


	#SERVER UPDATES/COMMANDS

	def build(self, name, x, y, z, userid, unitid, Protocol=None):
		pos = (int(x), int(y), int(z))
		userid = int(userid)
		unitid = int(unitid)
		shared.DPrint(0, "netUnitManager", "Erecting "+str(name)+" at "+str(pos))

		if name in self.unitscripts:
			owner = shared.PlayerManager.getFromUID(userid)
			newunit = self.unitscripts[name](unitid, owner, pos)
			owner.Units.append(newunit)

			if owner == shared.SelfPlayer:
				shared.DPrint(0, "netUnitManager", "The unit is ours "+str(userid)+" = "+str(shared.SelfPlayer.UID))
			else:
				shared.DPrint(0, "netUnitManager", "The unit is player "+str(owner.username)+" at team "+str(owner.team))

			if int(owner.team) == int(shared.SelfPlayer.team):
				shared.DPrint("netUnitManager", 0, "Adding unit as ally")
				newunit._fowview = shared.FowManager.addAlly(newunit._entity.node, 256)
			else:
				shared.DPrint("netUnitManager", 0, "Adding unit as enemy")
				newunit._fowview = shared.FowManager.addEnemy(newunit._entity.node)

			shared.FowManager.nodeUpdate(newunit._entity.node)

		else:
			shared.DPrint(5, "netUnitManager", "Unitscript for "+str(name)+" does not exsist!")
			print(self.unitscripts)

	
	def recv_unithealth(self, unitid, health, Protocol=False):
		unit = self.getFromUID(unitid)
		unit._setHealth(health)
		print("HEALTH: "+str(unit.ID)+" = "+str(health))


	#INTERNALS

	def getFromUID(self, UnitID, Player=None):
		#This function probleary needs to be optimized!
		if not Player:
			UnitID=int(UnitID)
			for Unit in shared.SelfPlayer.Units:
				print("UID: "+str(UnitID)+" / "+str(Unit.ID))
				if Unit.ID == UnitID:
					return Unit

			for PID, player in shared.PlayerManager.PDict.iteritems():
				for Unit in player.Units:
					print("UID: "+str(UnitID)+" / "+str(Unit.ID))
					if Unit.ID == UnitID:
						return Unit

		if Player:
			print("PLAYER: "+str(Player.Units))
			for unit in Player.Units:
				if int(unit.ID)==int(UnitID):
					return unit

		return False

