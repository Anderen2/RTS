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
		self.Actions={cl_act.Action}

	def OnCreation(self, pos):
		#self.PlayAnim("TakeOff") #Create a function/Class for simple movement animations
		self.GetEntity().actMove(True)

	def OnDie(self):
		#self.PlayAnim("SpiralDown") #Create a function/Class for simple movement animations
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

	def OnMove(self, pos):
		self.GetEntity().actMove(True)