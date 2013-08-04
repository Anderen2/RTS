#BaseUnit - Clientside
#This is the class which all units derive from and bases itself on
from traceback import print_exc
from engine import shared, debug
from engine.Object.unitact import cl_move, cl_fau

class BaseUnit():
	#Setup Constants
	MOVETYPE_AIR = 0
		
	def __init__(self, ID, owner, pos):
		#Setup variables
		self.ID=int(ID)
		self._owner=owner
		self._group=None
		self._text = ""

		#Actions
		self._currentaction=None
		self._globalactions = [cl_move.Action, cl_fau.Action]

		#Movement
		self._movetopoint=None

		#State
		self._health=100

		self.Initialize()
		shared.DPrint(0, "BaseUnit", "Initialized "+str(self.ID))
		self._setPosition(pos)
		self.OnCreation(pos)

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
		return True

	def GetMoveType(self):
		return MOVETYPE_AIR

	def GetMoveSpeed(self):
		return 100

	def GetHealth(self):
		return self._health

	def GetViewRange(self):
		return 100

	### Trigger Hooks

	def _selected(self):
		shared.DPrint("Globalunit",5,"Unit selected: "+str(self.ID))
		self._entity.text.enable(True)
		if debug.AABB:
			self._entity.node.showBoundingBox(True)

	def _deselected(self):
		shared.DPrint("Globalunit",5,"Unit deselected: "+str(self.ID))
		self._entity.text.enable(False)
		if debug.AABB:
			self._entity.node.showBoundingBox(False)

	def _think(self, delta):
		self._entity.text.setText(self._text+": HP "+str(self.GetHealth()))
		self._entity.text.update()
		self._entity.Think()
		if self._currentaction!=None:
			self._currentaction.update()

		if self._movetopoint!=None:
			dst = (self._movetopoint[0], self._movetopoint[2])
			dist = self._movestep(dst, delta)
			if dist<1:
				self._movetopoint=None

	### Internal Functions

	# Health
	def _setHealth(self, health):
		self._health=health
		if self._health<1:
			self.OnDie()
			self._die()

	def _die(self):
		self._group.rmUnit(self)
		self._owner.Units.remove(self)

	# Movement
	def _movestep(self, dst, delta):
		src = (self._pos[0], self._pos[2])
		speed = (self.GetMoveSpeed()*delta)
		nx, ny, dist = shared.Pathfinder.ABPath.GetNextCoord(src, dst, speed)
		newpos = (nx, self._pos[1], ny)
		
		self._setPosition(newpos)
		return dist

	def _moveto(self, pos):
		self._movetopoint=pos
		self._look(self._movetopoint)
		self.OnMove(pos)

	def _stopmove(self):
		self._movetopoint=None

	# ENTITY
	def _setPosition(self, pos):
		self._pos=pos
		self._entity.SetPosition(pos[0], pos[1], pos[2])
		if shared.FowManager!=None and shared.FowManager!=True:
			shared.FowManager.nodeUpdate(self._entity.node)

	def _getPosition(self):
		return (self._entity.node.getPosition().x, self._entity.node.getPosition().y, self._entity.node.getPosition().z)

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

	def _finishAction(self):
		if self._currentaction!=None:
			self._currentaction.finish()
			self._currentaction=None

	def _abortAction(self):
		if self._currentaction!=None:
			self._currentaction.abort()
			self._currentaction=None