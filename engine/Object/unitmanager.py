#Mainmodule - UnitManager
#This module keeps track of the different units on the map, 
#aswell as creating, destroying and managing them

from engine import shared, debug
from engine.shared import DPrint
from engine.Lib import YModConfig
from unit import movtype, stuctype
from ogre.renderer.OGRE import FrameListener

class UnitManager(FrameListener):
	def __init__(self):
		FrameListener.__init__(self)
		shared.DPrint("UnitManager",1,"Initializing..")
		self.units={}
		self.u2=[]
		self.ucount=0

	def PowerUp(self):
		#Load Unitfiles
		self.parser=YModConfig.Parser("Data/Unit/", "unit")
		self.UnitDict=self.parser.start()
		if self.UnitDict==False:
			shared.DPrint("UnitManager", 3, "Parsing files failed!")

	def GetParam(self, ent, key):
		return self.UnitDict[ent][key]

	def GetParams(self, ent):
		return self.UnitDict[ent]

	def Create(self, team, name, pos=None):
		if name in self.UnitDict:
			if self.UnitDict[name]["movable"]==0:
				return self.CreateStuc(self.UnitDict[name]["type"], self.UnitDict[name]["faction"], name, self.UnitDict[name]["ent"], pos)
			elif self.UnitDict[name]["movable"]==1:
				return self.CreateMov(self.UnitDict[name]["type"], self.UnitDict[name]["faction"], name, self.UnitDict[name]["ent"], pos)
		else:
			shared.DPrint("UnitManager",3,"Tried to create nonexsitant unit: "+str(name))
			return False

	def massMove(self, units, pos):
		for x in units:
			self.Get(x)._setwaypoint(pos)

	def CreateStuc(self, Type, Team, SubType, ent, pos=None):
		ID=self.ucount
		self.ucount+=1

		if Type==1:
			pointer=stuctype.Buildable(ID, Team, SubType, ent, pos)
		elif Type==2:
			pointer=stuctype.Bunker(ID, Team, SubType, ent, pos)
		elif Type==3:
			pointer=stuctype.Tech(ID, Team, SubType, ent, pos)

		self.units[ID]=pointer
		return pointer

	def CreateMov(self, Type, Team, SubType, ent, pos=None):
		ID=self.ucount
		self.ucount=self.ucount+1

		if Type==1:
			pointer=movtype.Worker(ID, Team, SubType, ent, pos)
		elif Type==2:
			pointer=movtype.Vehicle(ID, Team, SubType, ent, pos)
		elif Type==3:
			pointer=movtype.Infantry(ID, Team, SubType, ent, pos)
		elif Type==4:
			pointer=movtype.Aircraft(ID, Team, SubType, ent, pos)
		elif Type==5:
			pointer=movtype.Marine(ID, Team, SubType, ent, pos)
		else:
			pointer=movtype.Other(ID, Team, SubType, ent, pos)

		self.units[ID]=pointer
		print(self.units[ID])
		self.u2.append(pointer)
		return pointer

	def Delete(self, ID):
		del self.units[ID]

	def Count(self):
		return len(self.units)

	def Amount(self, SubType="", Team="", Faction="", Type=""):
		#Function to get how many units there are with the following attributes, and which units it is.
		tSubTypes={}
		tTeam={}
		tFaction={}
		tType={}
		
		for ID, x in self.units.items():
			if SubType!="" and SubType==x.subtype:
				if not x.subtype in tSubTypes:
					tSubTypes[SubType]={}
					tSubTypes[SubType]["count"]=1
					tSubTypes[SubType]["units"]=[x]
				else:
					tSubTypes[SubType]["count"]=tSubTypes[SubType]["count"]+1
					tSubTypes[SubType]["units"].append(x)

			if Team!="" and int(Team)==x.team:
				Team=int(Team)
				if not x.team in tTeam:
					tTeam[Team]={}
					tTeam[Team]["count"]=1
					tTeam[Team]["units"]=[x]
				else:
					tTeam[Team]["count"]=tTeam[Team]["count"]+1
					tTeam[Team]["units"].append(x)

			if Faction!="" and int(Faction)==x.faction:
				Faction=int(Faction)
				if not x.faction in tFaction:
					tFaction[Faction]={}
					tFaction[Faction]["count"]=1
					tFaction[Faction]["units"]=[x]
				else:
					tFaction[Faction]["count"]=tFaction[Faction]["count"]+1
					tFaction[Faction]["units"].append(x)

			if Type!="" and int(Type)==x.type:
				Type=int(Type)
				if not x.type in tType:
					tType[Type]={}
					tType[Type]["count"]=1
					tType[Type]["units"]=[x]
				else:
					tType[Type]["count"]=tType[Type]["count"]+1
					tType[Type]["units"].append(x)

		#ADD A SELECTIVE VALUE 
		#(AKA, a common value, "How many robot subtypes does player 1 have on the map;
		# How many USA aircrafts, how many factions are player 2 in control of ++ ")

		Total={}
		Total["SubTypes"]=tSubTypes
		Total["Teams"]=tTeam
		Total["Factions"]=tFaction
		Total["Types"]=tType

		return Total

	def Get(self, ID):
		return self.units[ID]

	def frameRenderingQueued(self, evt):
		for ID, unit in self.units.items():
			unit._think()

		return True

	def DeleteAll(self):
		for ID, unit in self.units.items():
			unit.__del__()
		self.units={}

	def __del__(self):
		pass