#Mainmodule - Props
#This module keeps track of the different props on the map, aswell as creating, destroying and managing them

from engine import shared, debug
from ogre.renderer.OGRE import FrameListener

class propManager(FrameListener):
	def __init__(self):
		FrameListener.__init__(self)
		shared.DPrint(7,1,"Initializing Prop Handeler")
		self.props={}
		self.dcount=0
		debug.ACC("p_c", self.Create, info="Create a prop on the map", args=1)

	def PowerUp(self):
		pass

	def Create(self, SubType):
		self.dcount=self.dcount+1
		ID=self.dcount-1

		pointer=Prop(ID, SubType)

		self.props[ID]=pointer

		return pointer

	def Destroy(self, ID):
		self.props[ID]._del()

	def Delete(self, ID):
		del self.props[ID]

	def Count(self):
		return len(self.props)

	def Amount(self, SubType="", Type=""):
		#Function to get how many props there are with the following attributes, and which props it is.
		tSubTypes={}
		tType={}
		
		for ID, x in self.props.items():
			if SubType!="" and SubType==x.subtype:
				if not x.subtype in tSubTypes:
					tSubTypes[SubType]={}
					tSubTypes[SubType]["count"]=1
					tSubTypes[SubType]["props"]=[x]
				else:
					tSubTypes[SubType]["count"]=tSubTypes[SubType]["count"]+1
					tSubTypes[SubType]["props"].append(x)

		#ADD A SELECTIVE VALUE 
		#(AKA, a common value, "How many robot subtypes does player 1 have on the map;
		# How many USA aircrafts, how many factions are player 2 in control of ++ ")

		Total={}
		Total["SubTypes"]=tSubTypes

		return Total

	def Get(self, ID):
		return self.props[ID]

	def frameRenderingQueued(self, evt):
		for ID, prop in self.props.items():
			prop._think()

		return True

	def _del(self):
		for ID, prop in self.props.items():
			prop._del()
		self.props={}

	def __del__(self):
		pass

#Propgroup:
class Prop():
	def __init__(self, ID, subtype):
		#Setup constants
		self.ID=ID
		self.subtype=subtype
		self.entity=None
		self.node=None
		self.text=None

		#Start rendering the prop (self, Identifyer, Type, Team, Interactive)
		self.entity=shared.EntityHandeler.Create(self.ID, self.subtype, "prop", None)

		#Do some post-render stuff
		self.entity.RandomPlacement()

		#Notify that we have successfuly created a prop!
		shared.DPrint(1,5,"Prop created! ID="+str(self.ID))

	def _think(self):
		pass

	def _selected(self):
		#This should never run, as props cannot be (de)selected
		shared.DPrint(1,5,"Prop selected: "+str(self.ID))

	def _deselected(self):
		#This should never run, as props cannot be (de)selected
		shared.DPrint(1,5,"Prop deselected: "+str(self.ID))

	def _setPos(self):
		pass

	def _del(self):
		shared.DPrint(1,5,"Prop deleted: "+str(self.ID))

		self.entity.Delete()
		shared.propHandeler.Delete(self.ID)

	def __del__(self):
		shared.DPrint(1,5,"Prop gc'd: "+str(self.ID))