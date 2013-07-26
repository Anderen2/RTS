#Clientside GroupManager
#This file handles the creation, management and utilization of networked unitgroups

import pickle

from twisted.internet import reactor
from engine import debug, shared

class GroupManager():
	def __init__(self):
		shared.GroupManager=self
		shared.objectManager.addEntry(0, 5, self)

		self.groups=[]
		self.groupspending=[]

	def req_newgroup(self, persistent, members):
		unitids = []
		for unit in members:
			unitids.append(unit.ID)

		print("UNITIDS: "+str(unitids))

		if len(unitids)>0:
			shared.protocol.sendMethod(5, "req_newgroup", [persistent, unitids])

			#Setting up tempoary clientside group
			tempgid = -(len(self.groupspending)+1)
			group = UnitGroup(tempgid, shared.SelfPlayer, persistent, members)
			self.groupspending.append(group)
			return group

	def recv_newgroup(self, gid, owner, persistent, pickleduids, Protocol=None):
		gid = int(gid)
		owner = shared.PlayerManager.getFromUID(owner)
		persistent = bool(int(persistent))
		units = self.unpackUnitList(pickleduids, owner)

		print("\n\nOWNER = "+str(owner))
		if owner == shared.SelfPlayer:
			group = self.groupspending.pop()
			group.gid=gid
			print("Got achnowlegde, newgid: "+str(gid))
			group.requestResend()
		else:
			group = UnitGroup(gid, owner, persistent, units)

		self.groups.append(group)

	def recv_addunits(self, gid, uidlist, Protocol=None):
		group = self.getFromGID(gid)
		units = unpackUnitList(uidlist, group.owner)
		for unit in units:
			group.addUnit(unit)

	def recv_rmunits(self, gid, uidlist, Protocol=None):
		group = self.getFromGID(gid)
		units = unpackUnitList(uidlist, group.owner)
		for unit in units:
			group.rmUnit(unit)

	def recv_setaction(self, gid, actionid, data, Protocol=None):
		print("Starting action: "+actionid+" w/ "+str(data))

	def recv_setactionstate(self, gid, state, Protocol=None):
		pass

	def recv_groupactionqueue(self, groupid, queue, Protocol=None):
		pass

	def unpackUnitList(self, uidlist, owner):
		units=[]
		for uid in uidlist:
			unit = shared.netUnitManager.getFromUID(uid, Player=owner)
			if unit!=False:
				units.append(unit)
			else:
				print("Could not find unit: "+str(uid)+" from player: "+owner.username)

		return units

	def getFromGID(self, gid):
		for group in self.groups:
			if group.gid == gid:
				return group

	def rmGroup(self, grp):
		remove = None
		if type(grp) == int:
			remove=self.getFromGID(grp)

		elif isinstance(grp, UnitGroup):
			if grp in self.groups:
				remove = grp

		if remove!=None:
			self.groups.remove(remove)

class UnitGroup():
	def __init__(self, gid, owner, persistent, members):
		self.members=members
		self.persistent=persistent
		self.owner = owner
		self.gid = gid
		self.actionQueue = []
		self.waitingfor = []

		#Simple workaround for those cases where the action get sent before the group is created
		self.actiondelay=[] 

		self.currentlyselected = False

		if self.persistent==True:
			self.owner.persistentgroups.append(self)

		for unit in self.members:
			unit._group=self

	## Group Requests
	def requestUnitAdd(self, unit):
		unitid = unit.ID
		shared.protocol.sendMethod(5, "req_addunits", [self.gid, [unitid]])

	def requestUnitRM(self, unit):
		unitid = unit.ID
		shared.protocol.sendMethod(5, "req_rmunits", [self.gid, [unitid]])

	def requestActionAdd(self, actionid, data):
		if self.gid<0:
			self.actiondelay.append((actionid, data))
		else:
			shared.protocol.sendMethod(5, "req_groupactionadd", [self.gid, actionid, data])

	def requestResend(self):
		for request in self.actiondelay:
			shared.protocol.sendMethod(5, "req_groupactionadd", [self.gid, request[0], request[1]])

	def requestActionAbort(self, action):
		pass

	def requestMove(self, pos):
		shared.protocol.sendMethod(5, "req_groupmove", [self.gid, pos])

	def requestPrimary(self):
		pass

	## Group Functions

	def addUnit(self, unit):
		self.members.append(unit)
		unit._group = self

	def rmUnit(self, unit):
		self.members.remove(unit)
		
		if unit._group == self:
			unit._group = None

		if len(self.members)==0 and self.persistent==False:
			shared.GroupManager.rmGroup(self)

	def addAction(self, action):
		self.actionQueue.append(action)
		print(self.actionQueue)
		self.updateVisuals()

	def rmAction(self, action):
		self.actionQueue.remove(action)
		self.updateVisuals()

	def setCurrentAction(self, action):
		pass

	def abortCurrentAction(self):
		pass

	def finishCurrentAction(self):
		pass

	## Visuals

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