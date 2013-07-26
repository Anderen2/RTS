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

	def build(self, name, x, y, z, userid, unitid, Protocol=None):
		pos = (int(x), int(y), int(z))
		userid = int(userid)
		unitid = int(unitid)
		shared.DPrint(0, "netUnitManager", "Erecting "+str(name)+" at "+str(pos))

		# if int(team) == int(shared.SelfPlayer.team):
		# 	shared.DPrint("netUnitManager", 0, "Adding unit as ally")
		# 	shared.FowManager.addAlly(unit.entity.node, 500)
		# else:
		# 	shared.DPrint("netUnitManager", 0, "Adding unit as enemy")
		# 	shared.FowManager.addEnemy(unit.entity.node)

		# shared.FowManager.nodeUpdate(unit.entity.node)

		if name in self.unitscripts:
			if userid==shared.SelfPlayer.UID:
				newunit = self.unitscripts[name](unitid, shared.SelfPlayer, pos)
				shared.SelfPlayer.Units.append(newunit)
				shared.DPrint(0, "netUnitManager", "The unit is ours "+str(userid)+" = "+str(shared.SelfPlayer.UID))
			else:
				owner = shared.PlayerManager.getFromUID(userid)
				newunit = self.unitscripts[name](unitid, owner, pos)
				owner.Units.append(newunit)
				shared.DPrint(0, "netUnitManager", "The unit is player "+str(owner.username)+" at team "+str(owner.team))

		else:
			shared.DPrint(5, "netUnitManager", "Unitscript for "+str(name)+" does not exsist!")
			print(self.unitscripts)

	def massmove(self, pickledunits, x, y, z, Protocol=None):
		units=pickledunits

		shared.unitManager.massMove(units, (float(x), float(y), float(z)))

	def getFromUID(self, UnitID, Player=None):
		#This function probleary needs to be optimized!
		if not Player:
			UnitID=int(UnitID)
			for Unit in shared.SelfPlayer.Units:
				print("UID: "+str(UnitID)+" / "+str(Unit.ID))
				if Unit.ID == UnitID:
					return Unit

			for PID, player in shared.PlayerManager.PDict.iteritems():
				print("UID: "+str(UnitID)+" / "+str(Unit.ID))
				for Unit in player.Units:
					if Unit.ID == UnitID:
						return Unit

		if Player:
			print("PLAYER: "+str(Player.Units))
			for unit in Player.Units:
				if int(unit.ID)==int(UnitID):
					return unit

		return False