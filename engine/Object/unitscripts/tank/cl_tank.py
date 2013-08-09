#Tank - Ground Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit

class Unit(BaseUnit):
	def Initialize(self):
		self.Name = "tank"
		self.SetEntity("tank")
		self.SetSelectedText("Tank "+str(self.GetID()))
		self.Actions=[]

	def OnCreation(self, pos):
		self.GetEntity().actNone()

	def OnDie(self):
		shared.EffectManager.Create("explosion", self._pos[0], self._pos[1], self._pos[2], 1, 1)
		self.GetEntity().actNone()
		self.GetEntity().actDead(True)

	def OnThink(self, delta):
		pass

	def OnPrimaryAction(self, unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def OnMoveEffectDone(self, moveeffect):
		pass

	def OnMove(self, pos):
		self.GetEntity().actMove(True)

	def AimAtUnit(self, unit):
		x, y, z = unit.GetEntity().GetPosition()
		self.GetEntity().rotTurretTowardPos(x, y, z)