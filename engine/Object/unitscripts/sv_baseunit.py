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
		self._currentaction=None
		self._globalactions = [sv_move.Action]

		self.Initialize()
		shared.DPrint(0, "BaseUnit", "Initialized "+str(self.ID))
		self._setposition(pos)
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

	def _think(self):
		if self._currentaction!=None:
			self._currentaction.update()

	def _actionfinish(self):
		if self._group!=None:
			self._group.actionDone(self._currentaction)

	### Internal Functions


	# MOVEMENT
	def _moveto(self, pos):
		pass

	def _stopmove(self):
		pass


	# ENTITY
	def _setposition(self, pos):
		self._pos = pos

	# ACTION
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