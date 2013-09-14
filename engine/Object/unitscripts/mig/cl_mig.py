#MIG - Air Unit
#Clientside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit
import cl_act

class Unit(BaseUnit):
	Name = "MIG"
	Description = "Type: Air Fighter\nEffective against Airunits, Armored Units"
	Image = "unit_mig"
	Buildtime = 5
	Cost = 750

	def Initialize(self, ID):
		self.SetEntity("plane")
		self.SetSelectedText("MIG "+str(self.GetID()))
		self.Actions=[cl_act.Action]

		self.Hook.Add("OnCreation", self.OnCreation)
		self.Hook.Add("OnDeath", self.OnDie)
		self.Hook.Add("OnMoveEffectDone", self.OnMoveEffectDone)
		self.Hook.Add("OnMove", self.OnMove)

	def OnCreation(self, pos):
		#self.PlayAnim("TakeOff") #Create a function/Class for simple movement animations
		self.GetEntity().actMove(True)

	def OnDie(self, cause):
		self.GetEntity().actNone()
		self.GetEntity().actDead(True)
		self.StartMoveEffect("globDiveDie")
	
	def _die(self):
		#We overwrite this as we take care of the death ourselves (See OnMoveEffectDone)
		pass

	def OnMoveEffectDone(self, moveeffect):
		if moveeffect=="globDiveDie":
			self.GetPosition()
			shared.EffectManager.Create("explosion", self._pos[0], self._pos[1], self._pos[2], 1, 1)
			self.Destroy()

	def OnMove(self, pos):
		self.GetEntity().actMove(True)

	#Action Triggers
	def OnPrimaryAction(self, unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def AimAtUnit(self, unit):
		x, y, z = unit.GetEntity().GetPosition()
		self.GetEntity().LookAtZ(x, y, z)