#Turret - Defence
#Clientside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit

from engine.Object.unitact import cl_fau, cl_const ## REMOVE LATER

class Unit(BaseUnit):
	Name = "Turret"
	Description = "Type: Ground Defence Unit\nEffective against both ground and air units"
	Image = "unit_turret"
	BuildEntity = "turret_build"
	Buildtime = 7
	Cost = 1000

	def Initialize(self, ID):
		self.SetEntity("turret")
		self.SetSelectedText("Turret "+str(self.GetID()))
		self.Actions=[]

		self.Hook.Add("OnCreation", self.OnCreation)
		self.Hook.Add("OnDeath", self.OnDie)
		self.Hook.Add("OnMove", self.OnMove)
		self.Hook.Add("OnMoveStop", self.OnIdle)

		#Overwrite GlobalActions [This should be changed for an less hackishlike solution]
		self._globalactions = [cl_fau.Action, cl_fau.Action, cl_const.Action]

	def OnCreation(self, pos):
		pass
		#self.GetEntity().actNone()

	def OnDie(self, cause):
		shared.EffectManager.Create("explosion", self._pos[0], self._pos[1], self._pos[2], 1, 1)
		self.GetEntity().actNone()
		self.GetEntity().actDead(True)

	def OnMove(self, pos):
		pass
		#self.GetEntity().actMove(True)

	def OnIdle(self, pos):
		pass
		#self.GetEntity().actIdle(True)

	#Action Triggers
	def OnPrimaryAction(self, unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def AimAtUnit(self, unit):
		x, y, z = unit._pos
		self.GetEntity().rotTurretTowardPos(x, y, z)
		print("Aiming..")