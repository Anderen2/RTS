#BaseUnit - Serverside
#This is the class which all units derive from and bases itself on
from traceback import print_exc
from importlib import import_module
from engine import shared, debug
from engine.Object.unitact import sv_move

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
		self._globalactions = [sv_move.Action]

		#Movement
		self._movetopoint=None

		self.Initialize()
		shared.DPrint(0, "BaseUnit", "Initialized "+str(self.ID))
		self._setPosition(pos)
		self.OnCreation(pos)

	### UnitScript Functions

	def SetEntity(self, ent):
		#Setup Pathfinding variables here (sizes, etc)
		self._entityname = ent
		shared.DPrint(0, "BaseUnit", "UnitID: "+str(self.ID)+" = "+str(ent))

	def SetSolid(self, yn):
		self._solidentity=yn

	def SetMoveType(self, movetype):
		#Setup Pathfinding algorthim based on the movetype here
		self._movetype = movetype

	def SetMoveSpeed(self, speed):
		#Setup Pathfinding movespeed here
		self._movespeed = speed

	def SetHealth(self, health):
		self._health = health

	def SetViewRange(self, viewrange):
		self._viewrange = viewrange

	def CreateProjectileLauncher(self):
		pass

	def SetAction(self, action, data):
		self._setAction(action, data)

	def GetAction(self):
		return self._currentaction

	### Trigger Hooks

	def _think(self, delta):
		if self._currentaction!=None:
			self._currentaction.update()

		if self._movetopoint!=None:
			dst = (self._movetopoint[0], self._movetopoint[2])
			dist = self._movestep(dst, delta)
			if dist<1:
				self._movetopoint=None

	def _actionfinish(self):
		if self._group!=None:
			self._group.unitActionDone(self)

	### Internal Functions


	# MOVEMENT
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
		self._currentaction=act(self, evt)
		self._currentaction.begin()

	def _endAction(self):
		self._currentaction=None