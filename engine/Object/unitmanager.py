#Mainmodule - UnitManager
#This module keeps track of the different units on the map, 
#aswell as creating, destroying and managing them

from engine import shared, debug
from engine.shared import DPrint
from unit import movtype, stuctype
from ogre.renderer.OGRE import FrameListener

class UnitManager(FrameListener):
	def __init__(self):
		FrameListener.__init__(self)
		shared.DPrint(6,1,"Initializing..")
		self.units={}
		self.ucount=0

	def PowerUp(self):
		pass

	def CreateMov(self, Type, Faction, Team, SubType):
		ID=self.ucount
		self.ucount=self.ucount+1

		if Type==1:
			pointer=movtype.Worker(ID, Faction, Team, SubType)
		elif Type==2:
			pointer=movtype.Vehicle(ID, Faction, Team, SubType)
		elif Type==3:
			pointer=movtype.Infantry(ID, Faction, Team, SubType)
		elif Type==4:
			pointer=movtype.Aircraft(ID, Faction, Team, SubType)
		elif Type==5:
			pointer=movtype.Marine(ID, Faction, Team, SubType)
		else:
			pointer=movtype.Other(ID, Faction, Team, SubType)

		self.units[ID]=pointer
		return pointer

	def CreateStuc(self, Type, Faction, Team, SubType):
		ID=self.ucount
		self.ucount+=1

		if Type==1:
			pointer=stuctype.Buildable(ID, Faction, Team, SubType)
		elif Type==2:
			pointer=stuctype.Bunker(ID, Faction, Team, SubType)
		elif Type==3:
			pointer=stuctype.Tech(ID, Faction, Team, SubType)

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