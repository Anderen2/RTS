#Build - Unit Structure
#Clientside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit
from engine.Object.unitact import cl_setway, cl_settarg
from engine.Object.unitscripts.build import cl_mig

class Unit(BaseUnit):
	def Initialize(self):
		self.Name = "build"
		self.SetEntity("house")
		self.SetSelectedText("BuildStructure: "+str(self.GetID()))
		self.Actions=[cl_mig.Action]

		self.Destination = None

		#Overwrite GlobalActions [This should be changed for an less hackishlike solution]
		self._globalactions = [cl_setway.Action, cl_settarg.Action]

	def OnCreation(self, pos):
		pass

	def OnDie(self):
		self.GetPosition()
		shared.EffectManager.Create("explosion", self._pos[0], self._pos[1], self._pos[2], 1, 1)
		return False #Return true here if you are handeling the destruction of the unit yourself (See OnMoveEffectDone)

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
		pass