#Mainmodule - Decorators
#This module keeps track of the different decorators on the map, aswell as creating, destroying and managing them

from engine import shared, debug
from ogre.renderer.OGRE import FrameListener

class DecoratorHandeler(FrameListener):
	def __init__(self):
		FrameListener.__init__(self)
		shared.DPrint(7,1,"Initializing..")
		self.decorators={}
		self.dcount=0

	def PowerUp(self):
		pass

	def Create(self, SubType):
		self.dcount=self.dcount+1
		ID=self.dcount-1

		if Type==1:
			pointer=Static(ID, SubType)
		elif Type==2:
			pointer=Tree(ID, SubType)
		elif Type==3:
			pointer=Physic(ID, SubType)
		elif Type==4:
			pointer=Water(ID, SubType)
		elif Type==5:
			pointer=Debris(ID, SubType)
		else:
			pointer=Other(ID, SubType)

		self.decorators[ID]=pointer

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

			if Type!="" and int(Type)==x.type:
				Type=int(Type)
				if not x.type in tType:
					tType[Type]={}
					tType[Type]["count"]=1
					tType[Type]["decorators"]=[x]
				else:
					tType[Type]["count"]=tType[Type]["count"]+1
					tType[Type]["decorators"].append(x)

		#ADD A SELECTIVE VALUE 
		#(AKA, a common value, "How many robot subtypes does player 1 have on the map;
		# How many USA aircrafts, how many factions are player 2 in control of ++ ")

		Total={}
		Total["SubTypes"]=tSubTypes
		Total["Types"]=tType

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

#Global Decoratorgroup:
class GlobalDecorator():
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
		shared.DPrint(1,5,"Decorator created! ID="+str(self.ID))

	def _think(self):
		# if self.entity.text:
		# 	self.entity.text.update()
		pass

	def _selected(self):
		shared.DPrint(1,5,"Decorator selected: "+str(self.ID))
		self.entity.text.enable(True)
		if debug.AABB:
			self.entity.node.showBoundingBox(True)

	def _deselected(self):
		shared.DPrint(1,5,"Decorator deselected: "+str(self.ID))
		self.entity.text.enable(False)
		self.entity.node.showBoundingBox(False)

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
		shared.DPrint(1,5,"Decorator deleted: "+str(self.ID))

		xExsist=None
		for x in shared.render3dSelectStuff.CurrentSelection:
			if self.node.getName() == x.getName():
				xExsist=x
		if xExsist!=None:
			shared.render3dSelectStuff.CurrentSelection.remove(xExsist)

		self.entity.Delete()
		shared.unitHandeler.Delete(self.ID)

	def __del__(self):
		shared.DPrint(1,5,"Decorator gc'd: "+str(self.ID))


#Type-dependant Decoratorgroups
class Static(GlobalDecorator):
	def init(self):
		self.type=1

class Tree(GlobalDecorator):
	def init(self):
		self.type=2

class Physic(GlobalDecorator):
	def init(self):
		self.type=3

class Water(GlobalDecorator):
	def init(self):
		self.type=4

class Debris(GlobalDecorator):
	def init(self):
		self.type=5

class Other(GlobalDecorator):
	def init(self):
		self.type=0