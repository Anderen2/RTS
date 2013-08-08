#MIG - Plane Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit
from migact import sv_act

#AddCSFile("cl_init.py")

class Unit(BaseUnit):
	def Initialize(self):
		self.Name = "MIG"
		self.SetEntity("plane")
		self.SetSolid(True)

		#self.Actions={"act1":{"name":"Action 1", "func":self.Act1, "GUI":1, "unique":"UniqueName"}}
		self.Actions=[sv_act.Action]
		#self.

		#self.SetMoveType(MOVETYPE_AIR)
		self.SetMoveType(0)
		self.SetMoveSpeed(100)
		self.SetHealth(100)
		self.SetViewRange(256)

		self.SetupProjectileLaunchers()

	def SetupProjectileLaunchers(self):
		self.Launcher1 = self.CreateProjectileLauncher(shared.LauncherManager.UNITLAUNCHER)
		self.Launcher1.SetPosition(0, 0, 0)
		self.Launcher1.SetRotation(10, 10, 10)
		self.Launcher1.SetProjectile("rocket")
		self.Launcher1.SetFireRange(1000)
		self.Launcher1.SetFiringSpeed(2)
		self.Launcher1.SetReloadingSpeed(5)
		self.Launcher1.SetMagasineCapasity(5)
		self.Launcher1.CanReloadLive(True)
		self.Launcher1.SetDamageRadius(1000)
		self.Launcher1.SetDamageHealth(10)
		self.Launcher1.SetRelativeDamage(False)

		self.Launcher2 = self.CreateProjectileLauncher(shared.LauncherManager.UNITLAUNCHER)
		self.Launcher2.SetPosition(10, 10, 10)
		self.Launcher2.SetRotation(30, 30, 30)
		self.Launcher2.SetProjectile("rocket")
		self.Launcher2.SetFireRange(1000)
		self.Launcher2.SetFiringSpeed(2)
		self.Launcher2.SetReloadingSpeed(5)
		self.Launcher2.SetMagasineCapasity(5)
		self.Launcher2.CanReloadLive(True)
		self.Launcher2.SetDamageRadius(1000)
		self.Launcher2.SetDamageHealth(10)
		self.Launcher2.SetRelativeDamage(False)

	def OnCreation(self, pos):
		th = shared.Map.Terrain.getHeightAtPos(pos[0], pos[2])
		ty = th+100
		self.SetPosition(pos[0], ty, pos[2])

	def OnDie(self):
		pass

	def OnThink(self, delta):
		pass

	def OnPrimaryAction(self, unit):
		# if unit.GetTeam()!=self.GetTeam():
		# 	if self.IsFreeSightTo(unit): 
		# 		if self.GetFireRange>self.GetDistanceTo(unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def PrimaryFire(self, unit):
		self.Launcher1.FireAtUnit(unit)
		self.Launcher2.FireAtUnit(unit)

	def OnMove(self, pos):
		pass