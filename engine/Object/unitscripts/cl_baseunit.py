#BaseUnit - Clientside
#This is the class which all units derive from and bases itself on
from sys import getrefcount
from random import randrange
from twisted.internet import reactor
from traceback import print_exc
from engine import shared, debug
from engine.shared import Vector
from engine.Lib.hook import Hook
from engine.Object.unitact import cl_move, cl_fau
from engine.Object import moveeff
from engine.World import movetypes

class BaseUnit():
	#Setup Constants
	MOVETYPE_AIR = 0
		
	def __init__(self, ID, owner, pos):
		#Setup variables
		self.ID=int(ID)
		self._owner=owner
		self._group=None
		self._text = ""

		#Initialize hooks
		self._inithooks()

		#Actions
		self._currentaction=None
		self._globalactions = [cl_move.Action, cl_fau.Action]

		#Movement
		self._movetopoint=None

		#MoveEffects
		self._currentmoveeff = None

		#State
		self._health=100 #Bogus value, Getting this from attributes instead See: UnitManager

		self.Initialize(self.ID)
		shared.DPrint(0, "BaseUnit", "Initialized "+str(self.ID))
		self._setPosition(pos)
		self.Hook.call("OnCreation", pos)

	def _inithooks(self):
		self.Hook = Hook(self)
		#Shared
		self.Hook.new("Initialize", 1)
		self.Hook.new("OnCreation", 1)
		self.Hook.new("OnThink", 1)
		self.Hook.new("OnHealthChange", 1)
		self.Hook.new("OnDamage", 2)
		self.Hook.new("OnDeath", 1)
		self.Hook.new("OnActionStart", 1)
		self.Hook.new("OnActionAbort", 1)
		self.Hook.new("OnActionFinished", 1)
		#self.Hook.new("OnActionState", 3) Currently Serverside Only
		self.Hook.new("OnServerUpdate", 1)
		self.Hook.new("OnGroupChange", 1)
		self.Hook.new("OnMove", 1)
		self.Hook.new("OnMoveStop", 1)
		self.Hook.new("OnConvertStart", 1)
		self.Hook.new("OnConverted", 1)

		#Clientside
		self.Hook.new("OnMoveEffectStart", 1)
		self.Hook.new("OnMoveEffectDone", 1)
		self.Hook.new("OnSelected", 0)
		self.Hook.new("OnDeselected", 0)

	### UnitScript Functions

	def GetID(self):
		return int(self.ID)

	def GetOwner(self):
		return self._owner

	def GetTeam(self):
		return self._owner.team

	def GetPosition(self):
		return self._getPosition()

	def SetEntity(self, ent):
		self._entityname = ent
		self._entity=shared.EntityHandeler.Create(self.ID, ent, "unit", self.GetTeam())
		try:
			if self._entity.error:
				shared.DPrint("Globalunit",4,"Entity error! Unit creation aborted!")
				self._del()

			self._entity.CreateTextOverlay()
		except:
			shared.DPrint("Globalunit",4,"Entity critical error! Unit creation aborted!")
			self._del()

	def GetEntity(self):
		return self._entity

	def SetSelectedText(self, text):
		self._text=text

	def GetSolid(self):
		return self._solidentity

	def GetMoveType(self):
		return MOVETYPE_AIR

	def GetMoveSpeed(self):
		return self._movespeed

	def GetHealth(self):
		return self._health

	def GetViewRange(self):
		return self._viewrange

	def StartMoveEffect(self, mveff):
		self._currentmoveeff = self._getMoveEffect(mveff)
		self.Hook.call("OnMoveEffectStart", mveff)

	def Destroy(self):
		self._rm()

	### Trigger Hooks

	def _selected(self):
		self.Hook.call("OnSelected")
		shared.DPrint("Globalunit",5,"Unit selected: "+str(self.ID))
		self._entity.text.enable(True)
		if debug.AABB:
			self._entity.node.showBoundingBox(True)

	def _deselected(self):
		self.Hook.call("OnDeselected")
		shared.DPrint("Globalunit",5,"Unit deselected: "+str(self.ID))
		self._entity.text.enable(False)
		if debug.AABB:
			self._entity.node.showBoundingBox(False)

	def _think(self, delta):
		self.Hook.call("OnThink", delta)
		self._entity.text.setText(self._text+": HP "+str(self.GetHealth()))
		self._entity.text.update()
		self._entity.Think()
		if self._currentaction!=None:
			self._currentaction.update()

		if self._movetopoint!=None:
			dist, newpos = movetypes.Move(self._pos, self._movetopoint, self._movespeed*delta, self._movetype)
			self._setPosition(newpos)
			if dist<1:
				self._stopmove()

		if self._currentmoveeff!=None:
			if self._currentmoveeff(self._entity, delta):
				self.Hook.call("OnMoveEffectDone", self._currentmoveeff.func_name)
				self._currentmoveeff=None

	### Internal Functions

	# Health
	def _setHealth(self, health):
		self.Hook.call("OnDamage", health, "DamageType Here!")
		self._health=health
		if self._health<1:
			self._predie()
			self.Hook.call("OnDeath", "LastDamageType Here!")
			self._die()

	def _predie(self):
		#Removing from interaction with game
		shared.DirectorManager.CurrentDirector.deselectUnit(self)
		if self._group:
			self._group.rmUnit(self)
		self._movetopoint=None

		if shared.FowManager!=None and shared.FowManager!=True:
			shared.FowManager.rmNode(self._entity.node)

	def _die(self):
		self._rm()

	def _rm(self):
		#Removing all visuals and itself
		self._owner.Units.remove(self)
		self._entity.Delete()
		print("Dead Referances: "+str(getrefcount(self)))

	# Movement
	def _moveto(self, pos):
		self._movetopoint=pos
		self._look(self._movetopoint)
		self.Hook.call("OnMove", pos)

	def _stopmove(self):
		self.Hook.call("OnMoveStop", self._movetopoint)
		self._movetopoint=None

	def _getMoveEffect(self, mveff):
		if mveff in dir(moveeff):
			return getattr(moveeff, mveff)

	# ENTITY
	def _setPosition(self, pos):
		self._pos=pos
		self._entity.SetPosition(pos[0], pos[1], pos[2])
		if shared.FowManager!=None and shared.FowManager!=True:
			shared.FowManager.nodeUpdate(self._entity.node)

	def _getPosition(self):
		self._pos = self._entity.GetPosition()
		return self._pos

	def _setrotation(self, rot):
		self._entity.Rotate(rot[0], rot[1], rot[2])

	def _look(self, pos):
		self._entity.LookAtZ(pos[0], pos[1], pos[2])

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
		self.Hook.call("OnActionStart", self._currentaction)

	def _finishAction(self):
		self.Hook.call("OnActionFinished", self._currentaction)
		if self._currentaction!=None:
			self._currentaction.finish()
			self._currentaction=None

	def _abortAction(self):
		self.Hook.call("OnActionAbort", self._currentaction)
		if self._currentaction!=None:
			self._currentaction.abort()
			self._currentaction=None

	# GROUP
	def _changegroup(self, newgroup):
		self.Hook.call("OnGroupChange", newgroup)
		print("CHANGING GROUP from "+str(self._group)+ " to "+str(newgroup))
		if self._group!=None:
			self._group.rmUnit(self)
		self._group=newgroup

	#Attributes
	def _attribUpdate(self, updated):
		self.Hook.call("OnServerUpdate", updated)
		if "pos" in updated:
			self._setPosition(self._pos)

		if "viewrange" in updated:
			if shared.FowManager!=None and shared.FowManager!=True:
				shared.FowManager.chViewSize(self._entity.node)

		if "entityname" in updated:
			pass #out

	#Other
	def _randomCallback(self, tmin, tmax, call):
		reactor.callLater(randrange(tmin, tmax, 1), call)