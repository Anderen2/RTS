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
		print("Starting action: "+str(actionid)+" w/ "+str(data))
		group = self.getFromGID(gid)
		group.finishCurrentAction()

		if actionid!=None:
			action = group.getActionByID(actionid)
			if action!=None:
				group.setCurrentAction(action, data)

	def recv_abortaction(self, gid, Protocol=None):
		group = self.getFromGID(gid)
		group.abortCurrentAction()

	def recv_setactionstate(self, gid, state, Protocol=None):
		pass

	def recv_groupactionqueue(self, groupid, queue, Protocol=None):
		group = self.getFromGID(groupid)
		ActionAndData = []
		for ActionID, Data in queue:
			ActionAndData.append((group.getActionByID(ActionID), Data))

		group.updateActionQueue(ActionAndData)

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

		self.getAllCommonActions()

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
			self.requestActionQueue()

	def requestResend(self):
		for request in self.actiondelay:
			shared.protocol.sendMethod(5, "req_groupactionadd", [self.gid, request[0], request[1]])

	def requestActionAbort(self, queuedactionid):
		shared.protocol.sendMethod(5, "req_groupactionrm", [self.gid, queuedactionid])
		self.requestActionQueue()

	def requestActionQueue(self):
		if self.gid>=0:
			#print("Requesting..")
			shared.protocol.sendMethod(5, "req_groupactionqueue", [self.gid])
			self.updateVisuals()
		else:
			print("Group is not ready yet: "+str(self.gid))

	## Group Functions

	def getActionByID(self, actionid):
		if actionid in self.allAvailibleActions:
			return self.allAvailibleActions[actionid][0]
		else:
			return None

	def getAllCommonActions(self):
		allUniqueActions=[]
		aUAWithUnit={}
		allCommonActions=[]
		ucount = 0
		for unit in self.members:
			for action in unit._getAllActions():
				if action.actionid not in allUniqueActions:
					allUniqueActions.append(action.actionid)
					aUAWithUnit[action.actionid]=(action, unit)
				if ucount==0:
					allCommonActions.append(action.actionid)
				else:
					if action.actionid not in allCommonActions:
						allCommonActions.remove(action.actionid)
			ucount+=1

		self.allUniqueActions=allUniqueActions
		self.allCommonActions=allCommonActions
		self.allAvailibleActions=aUAWithUnit

	## Unit Functions
	def addUnit(self, unit):
		self.members.append(unit)
		unit._group = self
		self.getAllCommonActions()
		self.updateSelectedVisuals()

	def rmUnit(self, unit):
		self.members.remove(unit)
		
		if unit._group == self:
			unit._group = None

		if len(self.members)==0 and self.persistent==False:
			shared.GroupManager.rmGroup(self)

		self.getAllCommonActions()
		self.updateSelectedVisuals()

	## Action Functions

	def setCurrentAction(self, action, data):
		self.waitingfor = []
		for unit in self.members:
			if action in unit._getAllActions():
				self.waitingfor.append(unit)
				unit._setAction(action, data)

		if self.owner==shared.SelfPlayer:
			if self.currentlyselected:
				self.requestActionQueue()

	def abortCurrentAction(self):
		for unit in self.waitingfor:
			unit._abortAction()

		if self.owner==shared.SelfPlayer:
			if self.currentlyselected:
				self.requestActionQueue()

	def finishCurrentAction(self):
		for unit in self.members:
			unit._finishAction()

	## ActionQueue Functions

	def updateActionQueue(self, ActionAndDataQueue):
		self.actionQueue = ActionAndDataQueue[:]
		if self.currentlyselected==True:
			self.updateVisuals()

	## Visuals

	def selected(self):
		self.currentlyselected=True
		self.updateSelectedVisuals()
		self.requestActionQueue()

	def deselected(self):
		self.currentlyselected=False
		self.updateSelectedVisuals()
		shared.WaypointManager.update(None, None)

	def guiCancelAction(self, aid):
		self.requestActionAbort(aid)

	def guiAddAction(self, actionid):
		self.requestActionAdd(actionid, {})

	def updateSelectedVisuals(self):
		if self.currentlyselected:
			buttonlist = []
			for actionid in self.allCommonActions:
				action = self.getActionByID(actionid)
				buttonlist.append((action.name, action.description, action.actguiPlacement, actionid))

			shared.gui['unitopt'].updateActions(self, buttonlist)

		else:
			shared.gui['unitopt'].updateActions(None, None)

	def updateVisuals(self):
		if self.currentlyselected:
			shared.gui['unitinfo'].updateQueue()

			#Update waypoints
			waypointdata = []

			for action, data in self.actionQueue:
				if "3dMouse" in data:
					wpdata = data["3dMouse"]
				elif "unitid" in data:
					unit = shared.netUnitManager.getFromUID(data["unitid"])
					if unit:
						wpdata = unit.GetPosition()
					else:
						continue
				else:
					wpdata = None
				print("\tAD: "+str((action.waypointType, wpdata)))
				waypointdata.append((action.waypointType, wpdata))

			shared.WaypointManager.update(self, waypointdata)