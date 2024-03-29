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
			actionidsAndData = []

			for actionAnddata in group.actionQueue:
				actionidsAndData.append((actionAnddata[0].actionid, actionAnddata[1]))

			Protocol.sendMethod(5, "recv_groupactionqueue", [group.gid, actionidsAndData])


	def req_groupactionadd(self, groupid, actionid, data, Protocol=None):
		group = self.getFromGID(groupid)
		requestingPlayer = shared.PlayerManager.getFromProto(Protocol)
		if group.owner == requestingPlayer:
			action = group.getActionByID(actionid)
			if action!=None:

				if "presend" in dir(action):
					presend = action.presend(group, data, "Add")
					if presend == None or type(presend)!=type(True):
						if presend!=None:
							data.update(presend)

						group.addAction(action, data)					
				else:
					group.addAction(action, data)

			else:
				print("Cannot find action!")
		else:
			print("Group is not owned by player!")

	def req_groupactionnow(self, groupid, actionid, data, Protocol=None):
		group = self.getFromGID(groupid)
		requestingPlayer = shared.PlayerManager.getFromProto(Protocol)
		if group.owner == requestingPlayer:
			action = group.getActionByID(actionid)
			if action!=None:

				if "presend" in dir(action):
					presend = action.presend(group, data, "Now")
					if presend == None or type(presend)!=type(True):
						if presend!=None:
							data.update(presend)

						group.addActionNow(action, data)					
				else:
					group.addActionNow(action, data)

			else:
				print("Cannot find action!")
		else:
			print("Group is not owned by player!")

	def req_groupactiondo(self, groupid, actionid, data, Protocol=None):
		group = self.getFromGID(groupid)
		requestingPlayer = shared.PlayerManager.getFromProto(Protocol)
		if group.owner == requestingPlayer:
			action = group.getActionByID(actionid)
			if action!=None:

				if "presend" in dir(action):
					presend = action.presend(group, data, "Do")
					if presend == None or type(presend)!=type(True):
						if presend!=None:
							data.update(presend)

						group.doAction(action, data)					
				else:
					group.doAction(action, data)

			else:
				print("Cannot find action!")
		else:
			print("Group is not owned by player!")

	def req_groupactionrm(self, groupid, queuedactionid, Protocol=None):
		group = self.getFromGID(groupid)
		requestingPlayer = shared.PlayerManager.getFromProto(Protocol)
		if group.owner == requestingPlayer:
				group.rmAction(queuedactionid)
		else:
			print("Group is not owned by player!")

	## INTERNALS
	def createGroup(self, persistent, units, player):
		gid = self.groupcount
		self.groupcount+=1

		group = UnitGroup(units, persistent, player, gid)
		self.groups.append(group)
		return group

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
			unit._changegroup(self)
			## Networking
			uidlist.append(unit.ID)

		shared.PlayerManager.Broadcast(5, "recv_newgroup", [self.gid, self.owner.UID, self.persistent, uidlist])

	def getCenterPosition(self):
		### Tempoary, does not yet get center position
		return self.members[0].GetPosition()

	def getAllCommonActions(self):
		allUniqueActions=[]
		aUAWithUnit={}
		allCommonActions={}
		ucount = 0
		for unit in self.members:
			allUnitActions = unit._getAllActions()
			allUnitActionsDict = {}
			for action in allUnitActions:
				allUnitActionsDict[action.actionid] = action
				if action.actionid not in allUniqueActions:
					allUniqueActions.append(action.actionid)
					aUAWithUnit[action.actionid]=(action, unit)
				if ucount==0:
					allCommonActions[action.actionid]=action

			nonCommonActions = []
			for actionName in allCommonActions:
				if actionName not in allUnitActionsDict:
					nonCommonActions.append(actionName)

			for nonCommonAction in nonCommonActions:
				del allCommonActions[nonCommonAction]

			ucount+=1

		self.allUniqueActions=allUniqueActions
		self.allCommonActions=allCommonActions
		self.allAvailibleActions=aUAWithUnit

	def addUnit(self, unit):
		self.members.append(unit)
		unit._changegroup(self)

		if len(self.actionQueue)!=0:
			if self.actionQueue[0][0] in unit.Actions:
				unit._setaction(self.actionQueue[0], self.actionQueue[0][1])

	def rmUnit(self, unit):
		self.members.remove(unit)
		
		if unit._group == self:
			unit._group = None

		if len(self.members)==0 and self.persistent==False:
			shared.GroupManager.rmGroup(self)

	def unitDown(self, unit):
		if unit in self.waitingfor:
			self.waitingfor.remove(unit)
		unit._abortAction()
		self.rmUnit(unit)

	def unitSwitchGroup(self, unit):
		if unit in self.waitingfor:
			self.waitingfor.remove(unit)
		unit._abortAction()
		self.rmUnit(unit)

	def getActionByID(self, actionid):
		## Algorithm to get all common actions here!
		self.getAllCommonActions()
		# print(self.members)
		# return self.members[0]._getActionByID(actionid)
		if actionid in self.allCommonActions:
			return self.allCommonActions[actionid]
		else:
			return None

	def actionIterator(self, action):
		for action in self.actionQueue:
			yield action[0]

	def getActionData(self, action):
		for actionAndData in self.actionQueue:
			if action == actionAndData[0]:
				return actionAndData

	#doAction simply makes all the units screw what ever they are doing, forget it and do the action
	def doAction(self, action, data):
		if len(self.actionQueue)==0 or self.actionQueue[0][0].abortable:
			if len(self.actionQueue)!=0:
				self.abortCurrentAction(wait=True)
			self.actionQueue=[]
			self.actionQueue.insert(0, (action, data))
			self.beginNextAction(doNotPop=True)

	#addActionNow allows the unit to "pause" the current action to do something else, for then to continue after it is done with the new action
	def addActionNow(self, action, data):
		if len(self.actionQueue)!=0:
			self.abortCurrentAction(wait=True)
		self.actionQueue.insert(0, (action, data))
		self.beginNextAction(doNotPop=True)

	#addAction puts the action at the end of their action queue, finishing all other actions before doing the new one
	def addAction(self, action, data):
		self.actionQueue.append((action, data))
		if self.actionQueue[0]==(action, data):
			print("I AM THE LAST ACTION!")
			self.beginNextAction(doNotPop=True)

	#instantAction makes the unit do the action instantly, but only if it has no other current actions in its queue
	def instantAction(self, action, data):
		if len(self.actionQueue)==0:
			self.actionQueue.append((action, data))
			self.beginNextAction(doNotPop=True)
		else:
			return False

	def rmAction(self, queuedactionid):
		if queuedactionid==0:
			if self.actionQueue[0][0].abortable:
				self.abortCurrentAction()
		else:
			self.actionQueue.pop(queuedactionid)

	def unitActionDone(self, unit):
		unit._finishAction() #We make the unit destroy its action and wait
		if unit in self.waitingfor:
			self.waitingfor.remove(unit)
			print("Unit not in waitingfor!")

		if len(self.waitingfor)==0:
			self.currentActionFinished()

	def currentActionFinished(self):
		self.beginNextAction()

	def abortCurrentAction(self, wait=False):
		for unit in self.waitingfor:
			unit._abortAction()

		print("\t Groupaction Aborted")
		shared.PlayerManager.Broadcast(5, "recv_abortaction", [self.gid])
		print("\t Groupaction Aborted - Next Action")
		if not wait:
			self.beginNextAction(False)
	
	def beginNextAction(self, doNotPop=False):
		if doNotPop==False:
			if len(self.actionQueue)!=0:
				self.actionQueue.pop(0)

		if len(self.actionQueue)>0:
			print("\t beginNextAction")
			action = self.actionQueue[0][0]
			data = self.actionQueue[0][1]

			self.waitingfor = []

			if "prebegin" in dir(action):
				prebegin = action.prebegin(self, self.members, data)
				if prebegin == None or type(prebegin)!=type(True):
					if prebegin!=None:
						data.update(prebegin)
					else:
						pass

					##SUCCESS

				elif prebegin == True:
					#Action cannot process at this time.
					return False
				elif prebegin == False:
					#Action cannot process because prebegin failed.
					return False

			for unit in self.members:
				if action in unit._getAllActions():
					self.waitingfor.append(unit)
					print("\t Setting action for member")
					unit._setAction(action, data)

				else:
					print("Unit is unable to execute action: "+str(action))
					pass
					#If one of the units in this group is missing the action which were requested ..
					# .. do not wait for him, and let him do nothing for the moment

			print("\t Broadcasting action")
			shared.PlayerManager.Broadcast(5, "recv_setaction", [self.gid, action.actionid, data])
		else:
			shared.PlayerManager.Broadcast(5, "recv_setaction", [self.gid, None, None])
		