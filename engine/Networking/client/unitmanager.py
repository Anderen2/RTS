#Clientside Unitmanager
from importlib import import_module
from engine import shared, debug
from engine.Object.unitscripts import cl_baseunit
from string import split

class UnitManager():
	def __init__(self):
		shared.netUnitManager=self
		shared.unitManager=self
		shared.unitHandeler=self
		shared.objectManager.addEntry(0,4, self)

		#self.unitregister={}
		self.unitscripts={}
		self.Load()

	def Load(self):
		#Find and import all availible UnitScripts HERE
		modpath = "engine.Object.unitscripts."
		self.unitscripts["mig"] = import_module(modpath+"mig.cl_mig").Unit
		self.unitscripts["build"] = import_module(modpath+"build.cl_build").Unit
		self.unitscripts["tank"] = import_module(modpath+"tank.cl_tank").Unit
		self.unitscripts["robot"] = import_module(modpath+"robot.cl_robot").Unit
		self.unitscripts["turret"] = import_module(modpath+"turret.cl_turret").Unit
		self.unitscripts["power"] = import_module(modpath+"power.cl_power").Unit
		self.unitscripts["derrick"] = import_module(modpath+"derrick.cl_derrick").Unit

	#SERVER UPDATES/COMMANDS

	def build(self, name, userid, unitid, attributes, Protocol=None):
		pos = attributes["pos"]
		userid = int(userid)
		unitid = int(unitid)
		shared.DPrint(0, "netUnitManager", "Erecting "+str(name)+" at "+str(pos))

		if name in self.unitscripts:
			#Creating unit
			owner = shared.PlayerManager.getFromUID(userid)
			newunit = self.unitscripts[name](unitid, owner, pos)
			owner.Units.append(newunit)

			#Setting up attributes
			for attribute, data in attributes.iteritems():
				if "." in attribute:
					foo = split(attribute, ".")
					subattr = getattr(newunit, "_"+foo[0])
					setattr(subattr, foo[1], data)
				else:
					setattr(newunit, "_"+attribute, data)

				print(attribute+" = "+str(data))

			#Giving the unit to its representative player
			if owner == shared.SelfPlayer:
				shared.DPrint(0, "netUnitManager", "The unit is ours "+str(userid)+" = "+str(shared.SelfPlayer.UID))
			else:
				shared.DPrint(0, "netUnitManager", "The unit is player "+str(owner.username)+" at team "+str(owner.team))

			#Updating the Fog Of War
			if int(owner.team) == int(shared.SelfPlayer.team):
				shared.DPrint("netUnitManager", 0, "Adding unit as ally")
				newunit._fowview = shared.FowManager.addAlly(newunit._entity.node, attributes["viewrange"])
			else:
				shared.DPrint("netUnitManager", 0, "Adding unit as enemy")
				newunit._fowview = shared.FowManager.addEnemy(newunit._entity.node)

			shared.FowManager.nodeUpdate(newunit._entity.node)

		else:
			shared.DPrint(5, "netUnitManager", "Unitscript for "+str(name)+" does not exsist!")
			print(self.unitscripts)

	
	def recv_unithealth(self, unitid, health, Protocol=False):
		unit = self.getFromUID(unitid)
		if unit:	
			unit._setHealth(health)
			print("HEALTH: "+str(unit.ID)+" = "+str(health))
		else:
			shared.DPrint(5, "netUnitManager", "Server sent healthupdate for non-exsistant unit!")

	def recv_updact(self, unitid, state, data, Protocol=False):
		unit = self.getFromUID(unitid)
		if unit._currentaction!=None:
			unit._currentaction.netupdate(state, data)
		else:
			shared.DPrint(5, "netUnitManager", "Server sent actionupdate for unit without any action!")

	def recv_attrib(self, unitid, attributes, Protocol=None):
		unit = self.getFromUID(unitid)
		if unit:
			for attribute, data in attributes.iteritems():
				if "." in attribute:
					foo = split(attribute, ".")
					subattr = getattr(unit, "_"+foo[0])
					setattr(subattr, foo[1], data)
				else:
					setattr(unit, "_"+attribute, data)

				print(attribute+" = "+str(data))
				unit._attribUpdate(attributes)
		else:
			shared.DPrint(5, "netUnitManager", "Server sent attributeupdate for non-exsistant unit!")


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

	def getUnit(self, UnitID):
		if UnitID in self.unitscripts:
			print("UnitID: "+UnitID)
			return self.unitscripts[UnitID]
		else:
			print("UnitID: "+UnitID+" not here!")
			return None