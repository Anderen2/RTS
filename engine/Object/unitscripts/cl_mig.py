#MIG - Plane Unit
#Clientside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit
from migact import cl_act

class Unit(BaseUnit):
	def Initialize(self):
		self.Name = "MIG"
		self.SetEntity("plane")
		self.SetSelectedText("MIG "+str(self.GetID()))
		self.Actions=[cl_act.Action]

	def OnCreation(self, pos):
		#self.PlayAnim("TakeOff") #Create a function/Class for simple movement animations
		self.GetEntity().actMove(True)

	def OnDie(self):
		self.GetEntity().actNone()
		self.GetEntity().actDead(True)
		self.StartMoveEffect("globDiveDie")
		return True #Return true here if you are handeling the destruction of the unit yourself (See OnMoveEffectDone)

	def OnThink(self, delta):
		pass

	def OnPrimaryAction(self, unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def OnMoveEffectDone(self, moveeffect):
		if moveeffect=="globDiveDie":
			self.GetPosition()
			shared.EffectManager.Create("explosion", self._pos[0], self._pos[1], self._pos[2], 1, 1)
			self.Destroy()

	def OnMove(self, pos):
		self.GetEntity().actMove(True)