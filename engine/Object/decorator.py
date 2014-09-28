#Mainmodule - Decorators
#This module keeps track of the different decorators on the map, aswell as creating, destroying and managing them

from engine import shared, debug
from engine.Lib import suf
from ogre.renderer.OGRE import FrameListener
import traceback

class DecoratorHandeler(FrameListener):
	def __init__(self):
		FrameListener.__init__(self)
		shared.DPrint("DecoratorHandeler",1,"Initializing New Decoration Handeler")
		self.customDecos={}
		self.decorators={}
		self.dcount=0

	def PowerUp(self):
		pass

	def Create(self, name, pos=None, rot=None):
		self.dcount=self.dcount+1
		ID=self.dcount-1

		pointer=Decoration(ID, name, pos, rot)

		self.decorators[ID]=pointer

		#if shared.Pathfinder.aStarPath != None:
		#	suf.WaitOneTick(shared.Pathfinder.aStarPath.calculateSceneNodeCost, pointer.entity.node) #We have to wait one Tick/Frame for Ogre to properly update the scenenodes AABB

		return pointer

	def CreateCustomPrefix(self, name, prefix, pos=None, rot=None):
		if len(prefix)!=4:
			print("Prefix must be 4 characters long!")
			raise NameError
			return False

		if not prefix in self.customDecos:
			self.customDecos[prefix]={}
			self.customDecos[prefix]["count"]=0
			self.customDecos[prefix]["decos"]={}
		self.customDecos[prefix]["count"]=self.customDecos[prefix]["count"]+1
		ID=self.customDecos[prefix]["count"]-1

		pointer=Decoration(ID, name, pos, rot, prefix=prefix)

		self.customDecos[prefix]["decos"][ID]=pointer

		#if shared.Pathfinder.aStarPath != None:
		#	suf.WaitOneTick(shared.Pathfinder.aStarPath.calculateSceneNodeCost, pointer.entity.node) #We have to wait one Tick/Frame for Ogre to properly update the scenenodes AABB

		return pointer

	def Remove(self, ID, prefix="deco"):
		if prefix=="deco":
			if ID in self.decorators:
				self.Destroy(self.decorators[ID])
				del self.decorators[ID]
		else:
			if ID in self.customDecos[prefix]["decos"]:
				self.Destroy(self.customDecos[prefix]["decos"][ID])
				del self.customDecos[prefix]["decos"][ID]

	def Destroy(self, deco):
		deco._del()

	def Delete(self, deco):
		del deco
		#self.dcount-=1

	def Count(self):
		return len(self.decorators)

	def Amount(self, name="", Type=""):
		#Function to get how many decorators there are with the following attributes, and which decorators it is.
		tnames={}
		tType={}
		
		for ID, x in self.decorators.items():
			if name!="" and name==x.name:
				if not x.name in tnames:
					tnames[name]={}
					tnames[name]["count"]=1
					tnames[name]["decorators"]=[x]
				else:
					tnames[name]["count"]=tnames[name]["count"]+1
					tnames[name]["decorators"].append(x)

		#ADD A SELECTIVE VALUE 
		#(AKA, a common value, "How many robot names does player 1 have on the map;
		# How many USA aircrafts, how many factions are player 2 in control of ++ ")

		Total={}
		Total["names"]=tnames

		return Total

	def Get(self, ID):
		return self.decorators[ID]

	def GetAll(self, name):
		prefix=name[:4]
		ID = int(name[4:])
		if prefix=="deco":
			return self.Get(ID)
		else:
			return self.customDecos[prefix]["decos"][ID]

	def frameRenderingQueued(self, evt):
		for ID, decorator in self.decorators.items():
			decorator._think()

		return True

	def _del(self):
		for ID, decorator in self.decorators.iteritems():
			decorator._del()

		for prefix, content in self.customDecos.iteritems():
			print prefix
			for ID, decorator in content["decos"].iteritems():
				print ID
				decorator._del()
		self.decorators={}

	def __del__(self):
		pass

#Decoratorgroup:
class Decoration():
	def __init__(self, ID, name, pos=None, rot=None, prefix="deco"):
		#Setup constants
		self.ID=ID
		self.name=name
		self.entity=None
		self.node=None
		self.text=None
		self.prefix=prefix

		#Start rendering the unit (self, Identifyer, Type, Team, Interactive)
		self.entity=shared.EntityHandeler.Create(self.ID, self.name, self.prefix, None)
		try:
			if self.entity.error:
				shared.DPrint("Decoration",4,"Entity error! Decorator creation aborted!")
				self._del()
		except:
			shared.DPrint("Decoration",4,"Entity critical error! Decorator creation aborted!")
			self._del()

		#Do some post-render stuff
		if pos==None:
			self.entity.RandomPlacement()
		else:
			print(pos)
			x, y, z = pos
			self._setPos(x, y, z)

		if rot!=None:
			print(rot)
			x, y, z = rot
			self._setRot(x, y, z)

		#Notify that we have successfuly created a unit!
		shared.DPrint("Decoration",5,"Decorator created! ID="+str(self.ID))

	def _think(self):
		pass

	def _selected(self):
		#This should never run ingame, as decs cannot be (de)selected. They can however in the mapeditor
		shared.DPrint("Decoration",5,"Decorator selected: "+str(self.ID))
		if self.entity!=None:
			self.entity.node.showBoundingBox(True)

	def _deselected(self):
		#This should never run ingame, as decs cannot be (de)selected. They can however in the mapeditor
		shared.DPrint("Decoration",5,"Decorator deselected: "+str(self.ID))
		if self.entity!=None:
			self.entity.node.showBoundingBox(False)

	def _setPos(self, x, y, z):
		self.entity.SetPosition(float(x), float(y), float(z))

	def _setRot(self, rotx, roty, rotz):
		self.entity.Rotate(float(rotx), float(roty), float(rotz))

	def _del(self):
		shared.DPrint("Decoration",5,"Decorator deleted: "+str(self.ID))

		try:
			xExsist=None
			for x in shared.render3dSelectStuff.CurrentSelection:
				if self.entity.node.getName() == x.getName():
					xExsist=x
			if xExsist!=None:
				shared.render3dSelectStuff.CurrentSelection.remove(xExsist)

			if not self.entity.error:
				self.entity.Delete()
				self.entity=None
			#shared.decHandeler.Delete(self.ID)
		except:
			shared.DPrint("Decoration",5,"Decorator Deletion Failed! Decorator may still be in memory and/or in game world!")
			traceback.print_exc()