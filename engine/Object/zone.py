#Mainmodule - Zones
#This module keeps track of the different zones on the map, aswell as creating, destroying and managing them

from engine import shared, debug
from ogre.renderer.OGRE import FrameListener

class zoneManager(FrameListener):
	def __init__(self):
		FrameListener.__init__(self)
		shared.DPrint(7,1,"Initializing Zone Handeler")
		self.zones={}
		self.dcount=0
		debug.ACC("z_c", self.Create, info="Create a zone on the map", args=3)

	def PowerUp(self):
		pass

	def Create(self, x, y, z):
		self.dcount=self.dcount+1
		ID=self.dcount-1

		pointer=Zone(ID, x, y, z)

		self.zones[ID]=pointer

		return pointer

	def Destroy(self, ID):
		self.zones[ID]._del()

	def Delete(self, ID):
		del self.zones[ID]

	def Count(self):
		return len(self.zones)

	def Amount(self, SubType="", Type=""):
		#Function to get how many zones there are with the following attributes, and which zones it is.
		tSubTypes={}
		tType={}
		
		for ID, x in self.zones.items():
			if SubType!="" and SubType==x.subtype:
				if not x.subtype in tSubTypes:
					tSubTypes[SubType]={}
					tSubTypes[SubType]["count"]=1
					tSubTypes[SubType]["zones"]=[x]
				else:
					tSubTypes[SubType]["count"]=tSubTypes[SubType]["count"]+1
					tSubTypes[SubType]["zones"].append(x)

		#ADD A SELECTIVE VALUE 
		#(AKA, a common value, "How many robot subtypes does player 1 have on the map;
		# How many USA aircrafts, how many factions are player 2 in control of ++ ")

		Total={}
		Total["SubTypes"]=tSubTypes

		return Total

	def Get(self, ID):
		return self.zones[ID]

	def frameRenderingQueued(self, evt):
		for ID, zone in self.zones.items():
			zone._think()

		return True

	def _del(self):
		for ID, zone in self.zones.items():
			zone._del()
		self.zones={}

	def __del__(self):
		pass

#Zonegroup:
class Zone():
	def __init__(self, ID, x, y, z):
		#Setup constants
		self.ID=ID
		self.x=x
		self.y=y
		self.z=z
		self.entity=None
		self.node=None
		self.text=None

		#Notify that we have successfuly created a zone!
		shared.DPrint(1,5,"Zone created! ID="+str(self.ID))

	def _think(self):
		pass

	def _selected(self):
		#This should never run, as Zones cannot be (de)selected
		shared.DPrint(1,5,"Zone selected: "+str(self.ID))

	def _deselected(self):
		#This should never run, as Zones cannot be (de)selected
		shared.DPrint(1,5,"Zone deselected: "+str(self.ID))

	def _setPos(self):
		pass

	def _del(self):
		shared.DPrint(1,5,"Zone deleted: "+str(self.ID))
		shared.zoneHandeler.Delete(self.ID)

	def __del__(self):
		shared.DPrint(1,5,"Zone gc'd: "+str(self.ID))