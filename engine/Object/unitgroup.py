#Unit Group
#UnitGroups is a way to optimalize networking when moving multiple units at the same time, aswell as a way to simplify Unit Actions, and Unit Queues

from engine import shared, debug
from engine.Object.unit import moveable, structure
from twisted.internet import reactor

class GroupManager():
	"""The only real goal with this manager is to keep Groups from getting unintentionaly GC'ed"""
	def __init__(self):
		self.groups=[]

	def newGroup(self, persistent=False, members=[]):
		group=UnitGroup(persistent, members)
		self.groups.append(group)
		return group

class UnitGroup():
	def __init__(self, persistent=False, members=[]):
		self.members=members
		if len(self.members)!=0:
			self.membertype=self.members[0].__class__

		self.persistent=persistent
		self.actionQueue=[]
		self.currentlyselected = False

	def addUnit(self, unit):
		if len(self.members)!=0:
			if isinstance(unit, moveable.Moveable):
				self.members.append(unit)
				if len(self.actionQueue)!=0:
					self.actionQueue[0].beginUnit(unit)

	def rmUnit(self, unit):
		unit.group = None
		self.delUnit(unit)

	def delUnit(self, unit):
		self.members.remove(unit)
		if len(self.members)==0 and self.persistent==False:
			shared.unitGroup.groups.remove(self)

	def addAction(self, action):
		self.actionQueue.append(action)
		if self.actionQueue[0]==action:
			self.beginNextAction()

		self.updateVisuals()

	def removeAction(self, action):
		if self.actionQueue[0] == action:
			self.actionQueue[0].abort()
			self.actionQueue.remove(action)
			self.beginNextAction()
		else:
			self.actionQueue.remove(action)

		self.updateVisuals()

	def removeActionID(self, actionid):
		if actionid == 0:
			self.actionQueue[0].abort()
			self.actionQueue.pop(actionid)
			self.beginNextAction()
		else:
			self.actionQueue.pop(actionid)

		self.updateVisuals()
		
	def actionFinished(self):
		self.actionQueue.pop(0)
		self.beginNextAction()
		self.updateVisuals()

	def beginNextAction(self):
		if len(self.actionQueue)!=0:
			self.actionQueue[0].begin()
			reactor.callLater(0.5, self.actionUpdate)

	def actionUpdate(self):
		if len(self.actionQueue)!=0:
			self.actionQueue[0].update()
		for unit in self.members:
			if unit.group!=self:
				self.delUnit(unit)

		reactor.callLater(0.5, self.actionUpdate)

	def selected(self):
		self.currentlyselected=True
		self.updateVisuals()

	def deselected(self):
		self.currentlyselected=False
		shared.WaypointManager.update(None)

	def updateVisuals(self):
		if shared.side=="Client":
			if self.currentlyselected:
				shared.gui['unitinfo'].updateQueue()
				#Update waypoints here
				shared.WaypointManager.update(self)