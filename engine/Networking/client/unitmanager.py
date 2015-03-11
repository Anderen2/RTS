#Clientside Unitmanager
from importlib import import_module
from engine import shared, debug
from engine.Object.unitscripts import cl_baseunit
from string import split
from os import listdir

class UnitManager():
	def __init__(self):
		shared.netUnitManager=self
		shared.unitManager=self
		shared.unitHandeler=self
		shared.objectManager.addEntry(0,4, self)

		#self.unitregister={}
		self.unitscripts={}
		self.Load()

		debug.ACC("unit_attrib", self.cmdGetAttributes, info="Get current attributes for unit\nUsage: unit_attrib unitid", args=1)
		debug.ACC("unit_attrib_test0", self.testClientAttrSync, args=2)

	def Load(self):
		#Find and import all availible UnitScripts HERE
		modpath = "engine.Object.unitscripts."
		filepath = "engine/Object/unitscripts/"
		# self.unitscripts["mig"] = import_module(modpath+"mig.cl_mig").Unit
		# self.unitscripts["build"] = import_module(modpath+"build.cl_build").Unit
		# self.unitscripts["tank"] = import_module(modpath+"tank.cl_tank").Unit
		# self.unitscripts["robot"] = import_module(modpath+"robot.cl_robot").Unit
		# self.unitscripts["turret"] = import_module(modpath+"turret.cl_turret").Unit
		# self.unitscripts["power"] = import_module(modpath+"power.cl_power").Unit
		# self.unitscripts["derrick"] = import_module(modpath+"derrick.cl_derrick").Unit

		for stuff in listdir(filepath):
			if not "." in stuff:
				self.unitscripts[stuff] = import_module(modpath+stuff+".cl_"+stuff).Unit

	#SERVER UPDATES/COMMANDS

	def build(self, name, userid, unitid, attributes, Protocol=None):
		pos = attributes["unit.position"]
		userid = int(userid)
		unitid = int(unitid)
		shared.DPrint(0, "netUnitManager", "Erecting "+str(name)+" at "+str(pos))

		if name in self.unitscripts:
			#Creating unit
			owner = shared.PlayerManager.getFromUID(userid)
			newunit = self.unitscripts[name](unitid, owner, pos)
			owner.Units.append(newunit)

			#Setting up attributes
			print("-"*5+"_serverAttributeSync"+"-"*5)
			print(attributes)
			newunit._serverAttributeSync(attributes, inital=True)

			#Giving the unit to its representative player
			if owner == shared.SelfPlayer:
				shared.DPrint(0, "netUnitManager", "The unit is ours "+str(userid)+" = "+str(shared.SelfPlayer.UID))
				self.getAttributeExtras(newunit)
			else:
				shared.DPrint(0, "netUnitManager", "The unit is player "+str(owner.username)+" at team "+str(owner.team))

			#Updating the Fog Of War
			if int(owner.team) == int(shared.SelfPlayer.team):
				shared.DPrint("netUnitManager", 0, "Adding unit as ally")
				newunit._fowview = shared.FowManager.addAlly(newunit._entity.node, newunit, attributes["unit.viewrange"])
			else:
				shared.DPrint("netUnitManager", 0, "Adding unit as enemy")
				newunit._fowview = shared.FowManager.addEnemy(newunit._entity.node, newunit)

			shared.FowManager.nodeUpdate(newunit._entity.node)

			#Updating the minimap
			print("Updating MinimapManager")
			UI = shared.MinimapManager.newUnitIndicator()
			UI.setUnit(newunit)

			

		else:
			shared.DPrint(5, "netUnitManager", "Unitscript for "+str(name)+" does not exsist!")
			print(self.unitscripts)


	def recv_updact(self, unitid, state, data, Protocol=False):
		unit = self.getFromUID(unitid)
		if unit._currentaction!=None:
			unit._currentaction.netupdate(state, data)
			shared.DPrint(0, "netUnitManager", "Recieved ActionState update '%s' from server" % state)
		else:
			shared.DPrint(5, "netUnitManager", "Server sent actionupdate for unit without any action!")

	def recv_attrib(self, unitid, attributes, Protocol=None):
		unit = self.getFromUID(unitid)
		if unit:
			unit._serverAttributeSync(attributes)
			shared.DPrint(0, "netUnitManager", "Recieved Attribute update from server")
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


	#Attributes

	def getAttributeExtras(self, unit):
		shared.protocol.sendMethod(4, "req_attrex", [unit.ID])

	def setAttribute(self, unit, attribute, value):
		shared.protocol.sendMethod(4, "req_setattr", [unit.ID, attribute, value])

	def recv_attrex(self, uid, attributeExtras, Protocol=None):
		self.getFromUID(uid).attributes["default"] = attributeExtras["default"]
		self.getFromUID(uid).attributes["readonly"] = attributeExtras["readonly"]


	def cmdGetAttributes(self, ID):
		unit = self.getFromUID(int(ID))

		self.getAttributeExtras(unit)

		current = ""
		for name, value in unit.attributes["current"].iteritems():
			current+="%s = %s\n" % (name, value)

		defaults = ""
		for name, value in unit.attributes["default"].iteritems():
			defaults+="%s = %s\n" % (name, value)

		readonly = ""
		for name, value in unit.attributes["readonly"].iteritems():
			if value==False:
				readonly+="%s = %s\n" % (name, value)

		NiceFormat = "Attributes for unit: (%s:%i)\nCurrent:\n%s\nDefaults:\n%s\nReadOnly:\n%s" % (unit.Name, unit.ID, current, defaults, readonly)

		print NiceFormat
		return NiceFormat

	def testClientAttrSync(self, uid, yn):
		if yn=="yes":
			self.setAttribute(self.getFromUID(int(uid)), "unit.autoengage", True)
		elif yn=="no":
			self.setAttribute(self.getFromUID(int(uid)), "unit.autoengage", False)
		else:
			self.setAttribute(self.getFromUID(int(uid)), "unit.health", 9999)