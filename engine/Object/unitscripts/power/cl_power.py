#Power - Structure
#Clientside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit

from engine.Object.unitact import cl_setway, cl_settarg, cl_const ## REMOVE LATER

import cl_upgrade

class Unit(BaseUnit):
	UnitID = "power"
	Name = "Power"
	Description = "Power Structure\nGives your base power"
	Image = "unit_power"
	BuildEntity = "power"
	Buildtime = 4
	Cost = 800

	def Initialize(self, ID):
		self.SetEntity("power")
		self.SetSelectedText("Power "+str(self.GetID()))
		self.Actions=[cl_upgrade.Action]

		self.Hook.Add("OnCreation", self.OnCreation)
		self.Hook.Add("OnDeath", self.OnDie)

		#Overwrite GlobalActions [This should be changed for an less hackishlike solution]
		self._globalactions = [cl_setway.Action, cl_settarg.Action, cl_const.Action]

	def OnCreation(self, pos):
		#Generate power
		pass
		
	def _die(self):
		#Workaround for video due to crashing when dying! FIX IT
		self._entity.node.setVisible(False)
		pass

	def OnDie(self, cause):
		shared.EffectManager.Create("atomic", self._pos[0], self._pos[1], self._pos[2], 0.05, 3)
		self.GetEntity().actNone()
		self.GetEntity().actDead(True)