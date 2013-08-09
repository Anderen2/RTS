#BaseUnit - Serverside
#This is the class which all units derive from and bases itself on
from traceback import print_exc
from importlib import import_module
from twisted.internet import reactor
from engine import shared, debug
from engine.Object.unitact import sv_move, sv_fau
from engine.World import movetypes

class BaseUnit():
	#Setup Constants
	MOVETYPE_AIR = 0
		
	def __init__(self, ID, owner, pos):
		#Setup variables
		self.ID=int(ID)
		self._owner=owner
		self._group=None

		#Actions
		self._currentaction=None
		self._globalactions = [sv_move.Action, sv_fau.Action]

		#Movement
		self._movetopoint=None

		#State
		self._health = 100
		self.pendingattrib={}

		self._setPosition(pos)
		self.Initialize()
		shared.DPrint(0, "BaseUnit", "Initialized "+str(self.ID))
		self.OnCreation(pos)

	### UnitScript Functions
	def SetPosition(self, x, y, z):
		self._setPosition((x,y,z))
		self._updateAttrib("pos", (x,y,z))

	def GetPosition(self):
		return self._pos

	def SetEntity(self, ent):
		#Setup Pathfinding variables here (sizes, etc)
		self._entityname = ent
		shared.DPrint(0, "BaseUnit", "UnitID: "+str(self.ID)+" = "+str(ent))
		self._updateAttrib("entityname", ent)

	def SetSolid(self, yn):
		self._solidentity=yn
		self._updateAttrib("solidentity", yn)

	def SetMoveType(self, movetype):
		#Setup Pathfinding algorthim based on the movetype here
		self._movetype = movetype
		self._updateAttrib("movetype", movetype)

	def SetMoveSpeed(self, speed):
		#Setup Pathfinding movespeed here
		self._movespeed = speed
		self._updateAttrib("movespeed", speed)

	def SetMaxHealth(self, health):
		self._health = health
		self._updateAttrib("health", health)

	def SetHealth(self, health):
		self._sethealth(health)

	def TakeDamage(self, damage):
		self._sethealth(self._health-damage)

	def SetViewRange(self, viewrange):
		self._viewrange = viewrange
		self._updateAttrib("viewrange", viewrange)

	def CreateProjectileLauncher(self, type):
		launcher = shared.LauncherManager.create(type, self)
		return launcher

	def SetAction(self, action, data):
		self._setAction(action, data)

	def GetAction(self):
		return self._currentaction

	def SetOwner(self, newowner):
		"""This is used if the unit is ex. captured by an another player"""
		pass

	### Trigger Hooks

	def _think(self, delta):
		if self._currentaction!=None:
			self._currentaction.update()

		if self._movetopoint!=None:
			dist, self._pos = movetypes.Move(self._pos, self._movetopoint, self._movespeed*delta, self._movetype)

			if dist<1:
				self._movetopoint=None

	def _actionfinish(self):
		if self._group!=None:
			self._group.unitActionDone(self)

	### Internal Functions

	## Networked

	#Unit Attributes
	def _updateAttrib(self, attribname, data):
		if len(self.pendingattrib)==0:
			#The reason for why we do this is to collect all attribute changes in one frame and send them all in one package.
			#As the client seemly only could recieve 60 pkgs each secound [With the current transferring method], we keep the packagequeue from getting too big
			reactor.callLater(0.5, self._broadcastAttrib)
		self.pendingattrib[attribname]=data

	def _broadcastAttrib(self):
		if len(self.pendingattrib)!=0:
			shared.PlayerManager.Broadcast(4, "recv_attrib", [self.ID, self.pendingattrib.copy()])
			self.pendingattrib={}

	#Health
	def _sethealth(self, health):
		if health != self._health:
			self._health = health
			shared.PlayerManager.Broadcast(4, "recv_unithealth", [self.ID, self._health])

		if health<1:
			self.OnDie()
			self._die()

	def _die(self):
		if self._group!=None:
			self._group.unitDown(self)
		self._owner.Units.remove(self)


	## NON-Networked (Mostly stuff handeled by the groupmanager instead)

	# MOVEMENT
	def _simulateMoveStep(self, dst, speed, src=None):
		if not src:
			src = (self._pos[0], self._pos[2])
		speed = speed
		nx, ny, dist = shared.Pathfinder.ABPath.GetNextCoord(src, dst, speed)
		newpos = (nx, self._pos[1], ny)

		return dist, newpos

	def _movestep(self, dst, delta):
		src = (self._pos[0], self._pos[2])
		speed = (self._movespeed*delta)
		nx, ny, dist = shared.Pathfinder.ABPath.GetNextCoord(src, dst, speed)
		newpos = (nx, self._pos[1], ny)
		
		self._setPosition(newpos)
		return dist

	def _moveto(self, pos):
		print("Moving unit: "+str(self.ID)+"to "+str(pos))
		self._movetopoint=pos
		self.OnMove(pos)

	def _stopmove(self):
		self._movetopoint=None


	# ENTITY
	def _setPosition(self, pos):
		self._pos = pos

	# ACTIONS
	def _loadActions(self):
		pass

	def _getActionByID(self, aid):
		for action in self._globalactions:
			if action.actionid == aid:
				return action

		for action in self.Actions:
			if action.actionid == aid:
				return action

	def _getAllActions(self):
		allactions = []
		allactions.extend(self._globalactions)
		allactions.extend(self.Actions)
		return allactions

	def _setAction(self, act, evt):
		if self._currentaction:
			self._currentaction.finish()
		self._currentaction=act(self, evt)
		self._currentaction.begin()

	def _finishAction(self):
		if self._currentaction!=None:
			self._currentaction.finish()
			self._currentaction=None

	def _abortAction(self):
		if self._currentaction!=None:
			self._currentaction.abort()
			self._currentaction=None

	def _sendActionState(self, state, data):
		shared.PlayerManager.Broadcast(4, "recv_updact", [self.ID, state, data])

	# GROUP
	def _changegroup(self, newgroup):
		print("CHANGING GROUP from "+str(self._group)+ " to "+str(newgroup))
		if self._group!=None:
			self._group.unitSwitchGroup(self)
		self._group=newgroup