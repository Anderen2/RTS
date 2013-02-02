#Mainmodule - Decorators
#This module keeps track of the different decorators on the map, aswell as creating, destroying and managing them

from engine import shared, debug
from ogre.renderer.OGRE import FrameListener

class DecoratorHandeler(FrameListener):
	def __init__(self):
		FrameListener.__init__(self)
		shared.DPrint("DecoratorHandeler",1,"Initializing New Decoration Handeler")
		self.decorators={}
		self.dcount=0

	def PowerUp(self):
		pass

	def Create(self, SubType):
		self.dcount=self.dcount+1
		ID=self.dcount-1

		pointer=Decoration(ID, SubType)

		self.decorators[ID]=pointer

		return pointer

	def Destroy(self, ID):
		self.decorators[ID]._del()

	def Delete(self, ID):
		del self.decorators[ID]

	def Count(self):
		return len(self.decorators)

	def Amount(self, SubType="", Type=""):
		#Function to get how many decorators there are with the following attributes, and which decorators it is.
		tSubTypes={}
		tType={}
		
		for ID, x in self.decorators.items():
			if SubType!="" and SubType==x.subtype:
				if not x.subtype in tSubTypes:
					tSubTypes[SubType]={}
					tSubTypes[SubType]["count"]=1
					tSubTypes[SubType]["decorators"]=[x]
				else:
					tSubTypes[SubType]["count"]=tSubTypes[SubType]["count"]+1
					tSubTypes[SubType]["decorators"].append(x)

		#ADD A SELECTIVE VALUE 
		#(AKA, a common value, "How many robot subtypes does player 1 have on the map;
		# How many USA aircrafts, how many factions are player 2 in control of ++ ")

		Total={}
		Total["SubTypes"]=tSubTypes

		return Total

	def Get(self, ID):
		return self.decorators[ID]

	def frameRenderingQueued(self, evt):
		for ID, unit in self.decorators.items():
			unit._think()

		return True

	def _del(self):
		for ID, unit in self.decorators.items():
			unit._del()
		self.decorators={}

	def __del__(self):
		pass

#Decoratorgroup:
class Decoration():
	def __init__(self, ID, subtype):
		#Setup constants
		self.ID=ID
		self.subtype=subtype
		self.entity=None
		self.node=None
		self.text=None

		#Start rendering the unit (self, Identifyer, Type, Team, Interactive)
		self.entity=shared.EntityHandeler.Create(self.ID, self.subtype, "decorator", None)

		#Do some post-render stuff
		self.entity.RandomPlacement()

		#Notify that we have successfuly created a unit!
		shared.DPrint("Decoration",5,"Decorator created! ID="+str(self.ID))

	def _think(self):
		pass

	def _selected(self):
		#This should never run, as decs cannot be (de)selected
		shared.DPrint("Decoration",5,"Decorator selected: "+str(self.ID))

	def _deselected(self):
		#This should never run, as decs cannot be (de)selected
		shared.DPrint("Decoration",5,"Decorator deselected: "+str(self.ID))

	def _setPos(self):
		pass

	def _del(self):
		shared.DPrint("Decoration",5,"Decorator deleted: "+str(self.ID))

		self.entity.Delete()
		shared.unitHandeler.Delete(self.ID)

	def __del__(self):
		shared.DPrint("Decoration",5,"Decorator gc'd: "+str(self.ID))