#Serverside vision Manager
#	This module handles the serverside implementation of the FogOfWar (FOW)
#	It also handles the quadtree logic for increasing unit lookup speed
#
#	This enables the server to only send updates on units for players who have them in their view,
#		aswell as decreasing performance usage for collision checking.

from engine.World import quadtree, posalgo
from engine import shared, debug

class VisionManager():
	def __init__(self):
		shared.VisionManager = self
		self.Units = {}

	def mapInitialize(self, size, max_objects=10):
		self.qtroot = quadtree.QuadTree(0, posalgo.Rectangle(0, 0, size, size), max_objects=max_objects)

	def addUnit(self, unit, viewrange):
		if not unit in self.Units:
			self.Units[unit]={}
		self.Units[unit]["view"] = FOVNode(viewrange, unit)
		self.Units[unit]["unit"] = UnitNode(unit)
	
	def addAimNode(self, unit, aimrange):
		if not unit in self.Units:
			self.Units[unit]={}
		self.Units[unit]["aim"] = AimRangeNode(aimrange, unit)

	def removeAimNode(self, unit):
		del self.Units[unit]["aim"]

	def rmUnit(self, unit):
		for stuff in self.Units[unit]:
			self.Units[unit][stuff].remove()

		del self.Units[unit]

	def unitUpdate(self, unit):
		pos = unit.GetPosition()
		unit._fovnode.setPosition((pos[0], pos[2]))
		unit._unitnode.setPosition((pos[0], pos[2]))
		if unit._autoengage:
			unit._aimnode.setPosition((pos[0], pos[2]))

			for oth in unit._aimnode.getAllInView():
				if oth._owner.team != unit._owner.team:
					if unit._group:
						print("AutoEngaging!")
						unit._group.instantAction(unit._globalactions[1], {"unitid":oth.ID})
			
	def getVisibleByPlayer(self, ply):
		pass
		#For unit in ply: Fovnode.getallinview

class FOVNode():
	def __init__(self, size, unit):
		self.size = size
		self.rectangle = posalgo.Rectangle(0, 0, size*2, size*2)
		shared.VisionManager.qtroot.insertObject(self, self.rectangle)
		# print self._qt_memberof
		# print len(self._qt_memberof)
		self.unit = unit
		self.unit._fovnode=self
		
	def getAllInView(self):
		inview = []
		center_pos = [self.rectangle.x + (self.rectangle.width / 2), self.rectangle.y + (self.rectangle.height / 2)]

		for obj in shared.VisionManager.qtroot.getAllObjectsInSameArea(self, objecttype=UnitNode):
			# print("AimRangeNode: Found object in QT-sector")
			pos = obj.unit.GetPosition()
			if posalgo.in_circle(center_pos[0], center_pos[1], self.size, pos[0], pos[2]):
				# print("AimRangeNode: Found object in circle")
				inview.append(obj.unit)

		return inview

	def setPosition(self, newpos):
		self.rectangle.x = newpos[0] - (self.rectangle.width / 2)
		self.rectangle.y = newpos[1] - (self.rectangle.height / 2)
		## HACKISH/SLOW: Reinsert object
		shared.VisionManager.qtroot.removeObject(self)
		shared.VisionManager.qtroot.insertObject(self, self.rectangle)

	def remove(self):
		self.unit._fovnode = None
		shared.VisionManager.qtroot.removeObject(self)

	#Use some fancy algorithms to circulize this bitch up, then get all QT-nodes it is an part of, and include it in all of them.  (No need, rectangles are precise enough)
	#Use posalgo in_circle to check for collisions

class AimRangeNode():
	def __init__(self, size, unit):
		self.size = size
		self.rectangle = posalgo.Rectangle(0, 0, size*2, size*2)
		shared.VisionManager.qtroot.insertObject(self, self.rectangle)
		self.unit = unit
		self.unit._aimnode=self
		
	def getAllInView(self):
		inview = []
		center_pos = [self.rectangle.x + (self.rectangle.width / 2), self.rectangle.y + (self.rectangle.height / 2)]

		for obj in shared.VisionManager.qtroot.getAllObjectsInSameArea(self, objecttype=UnitNode):
			# print("AimRangeNode: Found object in QT-sector")
			pos = obj.unit.GetPosition()
			if posalgo.in_circle(center_pos[0], center_pos[1], self.size, pos[0], pos[2]):
				# print("AimRangeNode: Found object in circle")
				inview.append(obj.unit)

		return inview

	def setPosition(self, newpos):
		self.rectangle.x = newpos[0] - (self.rectangle.width / 2)
		self.rectangle.y = newpos[1] - (self.rectangle.height / 2)
		## HACKISH/SLOW: Reinsert object
		shared.VisionManager.qtroot.removeObject(self)
		shared.VisionManager.qtroot.insertObject(self, self.rectangle)

	def remove(self):
		self.unit._aimnode=None
		shared.VisionManager.qtroot.removeObject(self)

class UnitNode():
	def __init__(self, unit):
		self.unit = unit
		self.unit._unitnode=self
		self.rectangle = posalgo.Rectangle(0, 0, 1, 1)
		shared.VisionManager.qtroot.insertObject(self, self.rectangle)

	def setPosition(self, newpos):
		self.rectangle.x = newpos[0] - (self.rectangle.width / 2)
		self.rectangle.y = newpos[1] - (self.rectangle.height / 2)
		## HACKISH/SLOW: Reinsert object
		shared.VisionManager.qtroot.removeObject(self)
		shared.VisionManager.qtroot.insertObject(self, self.rectangle)

	def remove(self):
		self.unit._unitnode=None
		shared.VisionManager.qtroot.removeObject(self)

