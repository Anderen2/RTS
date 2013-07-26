#Serverside GroupManager
#This file handles the creation, management and utilization of networked unitgroups

from twisted.internet import reactor
from engine import debug, shared

class GroupManager():
	def __init__(self):
		shared.GroupManager=self
		shared.objectManager.addEntry(0, 5, self)

		self.groups=[]
		self.groupcount = 0

	## CLIENT REQUESTS
	def req_newgroup(self, persistent, uidlist, Protocol=None):
		owner = shared.PlayerManager.getFromProto(Protocol)
		persistent=persistent
		gid = self.groupcount
		self.groupcount+=1
		#print("UIDLIST:"+ str(uidlist))
		units = self.unpackUnitList(uidlist, owner)

		group = UnitGroup(units, persistent, owner, gid)
		self.groups.append(group)

	# UNITS
	def req_addunits(self, groupid, pickleduids, Protocol=None):
		group = self.getFromGID(groupid)
		requestingPlayer = shared.PlayerManager.getFromProto(Protocol)
		if group.owner == requestingPlayer:
			units = self.unpackUnitList(pickleduids, requestingPlayer)

			for unit in units:
				if unit.owner == requestingPlayer:
					group.addUnit(unit)
				else:
					print("User: "+requestingPlayer.username+" tried to add user: "
						+unit.owner.username+"'s "+unit.Name+" to his group with ID: "
						+str(group.gid))

		else:
			print("User: "+requestingPlayer.username+" tried to add units to group which is owned by"
				+group.owner.username)

	def req_rmunits(self, groupid, pickleduids, Protocol=None):
		group = self.getFromGID(groupid)
		requestingPlayer = shared.PlayerManager.getFromProto(Protocol)
		if group.owner == requestingPlayer:
			units = self.unpackUnitList(pickleduids, requestingPlayer)

			for unit in units:
				group.rmUnit(unit)

		else:
			print("User: "+requestingPlayer.username+" tried to remove units from group which is owned by"
				+group.owner.username)

	# ACTIONS
	def req_groupactionqueue(self, groupid, Protocol=None):
		group = self.getFromGID(groupid)
		requestingPlayer = shared.PlayerManager.getFromProto(Protocol)
		if group.owner == requestingPlayer:
			actionids = []

			for action in group.actionQueue:
				actionids.append(action.actionid)

			Protocol.sendMethod(5, "recv_groupactionqueue", [group.gid, actionids])


	def req_groupactionadd(self, groupid, actionid, data, Protocol=None):
		group = self.getFromGID(groupid)
		requestingPlayer = shared.PlayerManager.getFromProto(Protocol)
		if group.owner == requestingPlayer:
			action = group.getActionByID(actionid)
			if action!=None:
				group.addAction(action, data)
			else:
				print("Cannot find action!")
		else:
			print("Group is not owned by player!")

	## FUNCTIONS

	def unpackUnitList(self, uidlist, owner):
		units=[]
		#print("Unpacking Unitlist")
		for uid in uidlist:
			unit = shared.UnitManager.getFromUID(uid, Player=owner)
			#print(unit)
			if unit!=False:
				units.append(unit)
			else:
				print("Could not find unit: "+str(uid)+" from player: "+owner.username)

		#print("UNITS-LIST: "+str(units))
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
	def __init__(self, members, persistent, owner, gid):
		self.members=members
		self.persistent=persistent
		self.owner = owner
		self.gid = gid
		self.actionQueue = []
		self.waitingfor = []

		if self.persistent==True:
			self.owner.persistentgroups.append(self)

		
		uidlist = []
		for unit in members:
			unit._group = self
			## Networking
			uidlist.append(unit.ID)

		shared.PlayerManager.Broadcast(5, "recv_newgroup", [self.gid, self.owner.UID, self.persistent, uidlist])

	def addUnit(self, unit):
		self.members.append(unit)
		unit._group = self

		if len(self.actionQueue)!=0:
			if self.actionQueue[0][0] in unit.Actions:
				unit._setaction(self.actionQueue[0], self.actionQueue[0][1])

	def rmUnit(self, unit):
		self.members.remove(unit)
		
		if unit._group == self:
			unit._group = None

		if len(self.members)==0 and self.persistent==False:
			shared.GroupManager.rmGroup(self)

	def getActionByID(self, actionid):
		## Algorithm to get all common actions here!
		print(self.members)
		return self.members[0]._getActionByID(actionid)

	def actionIterator(self, action):
		for action in self.actionQueue:
			yield action[0]

	def getActionData(self, action):
		for actionAndData in self.actionQueue:
			if action == actionAndData[0]:
				return actionAndData

	def addAction(self, action, data):
		self.actionQueue.append((action, data))
		if self.actionQueue[0]==(action, data):
			self.beginNextAction(doNotPop=True)

	def rmAction(self, action):
		if self.actionQueue[0][0] == action:
			self.abortCurrentAction()
		else:
			self.actionQueue.remove(getActionData(action))

	def unitActionDone(self, unit):
		self.waitingfor.remove(unit)
		if len(self.waitingfor)==0:
			self.currentActionFinished()

	def currentActionFinished(self):
		self.beginNextAction()

	def abortCurrentAction(self):
		for unit in self.waitingfor:
			unit._abortaction()

		self.beginNextAction()
	
	def beginNextAction(self, doNotPop=False):
		if len(self.actionQueue)>0:
			if doNotPop==False:
				self.actionQueue.pop(0)
			action = self.actionQueue[0][0]
			data = self.actionQueue[0][1]
			print("GROUPMEMBERS: "+str(self.members))
			for unit in self.members:
				if action in unit._getAllActions():
					self.waitingfor.append(unit)
					unit._setAction(action, data)
					shared.PlayerManager.Broadcast(5, "recv_setaction", [self.gid, action.actionid, data])

				else:
					print("Unit is unable to execute action: "+str(action))
					pass
					#If one of the units in this group is missing the action which were requested ..
					# .. do not wait for him, and let him do nothing for the moment