#Tank - Ground Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit

class Unit(BaseUnit):

	def Initialize(self, ID):
		self.Name = "tank"
		self.SetEntity("tank")
		self.SetSelectedText("Tank "+str(self.GetID()))
		self.Actions=[]

		self.Hook.Add("OnCreation", self.OnCreation)
		self.Hook.Add("OnDeath", self.OnDie)
		self.Hook.Add("OnMove", self.OnMove)
		self.Hook.Add("OnMoveStop", self.OnIdle)

	def OnCreation(self, pos):
		self.GetEntity().actNone()

	def OnDie(self, cause):
		shared.EffectManager.Create("explosion", self._pos[0], self._pos[1], self._pos[2], 1, 1)
		self.GetEntity().actNone()
		self.GetEntity().actDead(True)

	def OnMove(self, pos):
		self.GetEntity().actMove(True)

	def OnIdle(self, pos):
		self.GetEntity().actIdle(True)

	#Action Triggers
	def OnPrimaryAction(self, unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def AimAtUnit(self, unit):
		x, y, z = unit.GetEntity().GetPosition()
		self.GetEntity().rotTurretTowardPos(x, y, z)