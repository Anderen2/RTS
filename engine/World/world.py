#Mainmodule - World
#This module keeps track of the different decorators on the map, aswell as creating, destroying and managing them

from engine import shared, debug
from ogre.renderer.OGRE import FrameListener

class UnitHandeler(FrameListener):
	def __init__(self):
		FrameListener.__init__(self)
		shared.DPrint(7,1,"Initializing..")
		self.decorators={}
		self.dcount=0

	def PowerUp(self):
		pass

	def Create(self, Type, Faction, Team, SubType):
		self.ucount=self.ucount+1
		ID=self.ucount-1

		if Type==1:
			pointer=Worker(ID, Faction, Team, SubType)
		elif Type==2:
			pointer=Vehicle(ID, Faction, Team, SubType)
		elif Type==3:
			pointer=Infantry(ID, Faction, Team, SubType)
		elif Type==4:
			pointer=Aircraft(ID, Faction, Team, SubType)
		elif Type==5:
			pointer=Marine(ID, Faction, Team, SubType)
		else:
			pointer=Other(ID, Faction, Team, SubType)

		self.units[ID]=pointer

	def Destroy(self, ID):
		self.units[ID]._del()

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

	def _del(self):
		for ID, unit in self.units.items():
			unit._del()
		self.units={}

	def __del__(self):
		pass

#Global Unitgroup:
class GlobalUnit():
	def __init__(self, ID, faction, team, subtype):
		#Setup constants
		self.ID=ID
		self.faction=faction
		self.team=team
		self.subtype=subtype
		self.entity=None
		self.node=None
		self.text=None

		#Start rendering the unit
		shared.render3dScene.CreateEnt(self.subtype, self.team, ID, self)

		#Do some post-render stuff
		self.text.setText(subtype+" "+str(ID))

		#Start unit-dependant shit:
		self.init()

		#Notify that we have successfuly created a unit!
		shared.DPrint(1,5,"Unit created! ID="+str(self.ID))

	def _think(self):
		self.text.update()

	def _selected(self):
		shared.DPrint(1,5,"Unit selected: "+str(self.ID))
		self.text.enable(True)
		if debug.AABB:
			self.node.showBoundingBox(True)

	def _deselected(self):
		shared.DPrint(1,5,"Unit deselected: "+str(self.ID))
		self.text.enable(False)
		self.node.showBoundingBox(False)

	def _setPos(self):
		pass

	def _move(self):
		pass

	def _fire(self):
		pass

	def _damage(self, dmg):
		pass

	def _dead(self):
		pass

	def _del(self):
		shared.DPrint(1,5,"Unit deleted: "+str(self.ID))

		xExsist=None
		for x in shared.render3dSelectStuff.CurrentSelection:
			if self.node.getName() == x.getName():
				xExsist=x
		if xExsist!=None:
			shared.render3dSelectStuff.CurrentSelection.remove(xExsist)

		shared.render3dScene.DestroyEnt(self.entity, self.node, self.text)
		shared.unitHandeler.Delete(self.ID)

	def __del__(self):
		shared.DPrint(1,5,"Unit gc'd: "+str(self.ID))


#Type-dependant Unitgroups
class Worker(GlobalUnit):
	def init(self):
		self.type=1

class Vehicle(GlobalUnit):
	def init(self):
		self.type=2

class Infantry(GlobalUnit):
	def init(self):
		self.type=3

class Aircraft(GlobalUnit):
	def init(self):
		self.type=4

class Marine(GlobalUnit):
	def init(self):
		self.type=5

class Other(GlobalUnit):
	def init(self):
		self.type=0