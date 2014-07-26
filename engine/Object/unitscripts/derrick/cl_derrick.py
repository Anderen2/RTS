#Derrick - Structure
#Clientside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit

from engine.Object.unitact import cl_setway, cl_settarg, cl_const ## REMOVE LATER

class Unit(BaseUnit):
	Name = "Oil Derrick"
	Description = "Oil Derrick\nGenerates money"
	Image = "unit_derrick"
	BuildEntity = "derrick"
	Buildtime = 4
	Cost = 800

	def Initialize(self, ID):
		self.SetEntity("derrick")
		self.SetSelectedText("Derrick "+str(self.GetID()))
		self.Actions=[]

		self.Hook.Add("OnCreation", self.OnCreation)
		self.Hook.Add("OnDeath", self.OnDie)

		#Overwrite GlobalActions [This should be changed for an less hackishlike solution]
		self._globalactions = [cl_setway.Action, cl_settarg.Action, cl_const.Action]

	def OnCreation(self, pos):
		#Generate power
		pass
		

	def OnDie(self, cause):
		shared.EffectManager.Create("explosion", self._pos[0], self._pos[1], self._pos[2], 1, 1)
		self.GetEntity().actNone()
		self.GetEntity().actDead(True)