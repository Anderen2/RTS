#BaseUnit - Clientside
#This is the class which all units derive from and bases itself on
from traceback import print_exc
from engine import shared, debug

class BaseUnit():
	#Setup Constants
	MOVETYPE_AIR = 0
		
	def __init__(self, ID, owner, pos):
		#Setup variables
		self.ID=int(ID)
		self._owner=owner
		self._group=None

		self.Initialize()
		self._setposition(pos)
		self.OnCreation(pos)

	### UnitScript Functions

	def GetID(self):
		return int(self.ID)

	def GetOwner(self):
		return self._owner

	def GetTeam(self):
		return self._owner.team

	def GetPosition(self):
		return self._pos

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
		self._entity.text.setText(text+": HP "+str(self.GetHealth()))

	def GetSolid(self):
		return True

	def GetMoveType(self):
		return MOVETYPE_AIR

	def GetMoveSpeed(self):
		return 1

	def GetHealth(self):
		return 100

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

	def _think(self):
		self._entity.text.update()
		self._entity.Think()

	### Internal Functions

	def _setposition(self, pos):
		self._pos=pos
		self._entity.SetPosition(pos[0], pos[1], pos[2])
		#if shared.FowManager!=None and shared.FowManager!=True:
		#	shared.FowManager.nodeUpdate(self.entity.node)

	def _setrotation(self, rot):
		self._entity.Rotate(rot[0], rot[1], rot[2])

	def _look(self, x, y, z):
		self._entity.LookAtZ(x, y, z)

	def _setaction(self, act, evt):
		pass