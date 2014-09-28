#Tank - Ground Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit

from engine.Object.unitact import sv_fau, sv_const ## REMOVE LATER

#AddCSFile("cl_init.py")

class Unit(BaseUnit):
	UnitID = "turret"
	Name = "Turret"
	Description = "Type: Ground Defence Unit\nEffective against both ground and air units"
	Image = "unit_turret"
	Buildtime = 7
	Cost = 1000

	def Initialize(self, ID):
		self.SetEntity("turret")
		self.SetSolid(True)

		self.Actions=[]

		self.SetMoveType(-1) #MOVETYPE_GROUND
		self.SetMoveSpeed(0)
		self.SetHealth(1000)
		self.SetViewRange(1000)

		#Overwrite GlobalActions [This should be changed for an less hackishlike solution]
		self._globalactions = [sv_fau.Action, sv_fau.Action, sv_const.Action]

		self.Hook.Add("OnCreation", self.OnCreation)

	def SetupProjectileLaunchers(self):
		self.Launcher1 = self.CreateProjectileLauncher(shared.LauncherManager.UNITLAUNCHER)
		self.Launcher1.SetPosition(-10, 35, 12)
		self.Launcher1.SetRotation(0, 0, 0)
		self.Launcher1.SetProjectile("rocket")
		self.Launcher1.SetFireRange(700)
		self.Launcher1.SetFiringSpeed(2)
		self.Launcher1.SetReloadingSpeed(5)
		self.Launcher1.SetMagasineCapasity(-1)
		self.Launcher1.CanReloadLive(True)
		self.Launcher1.SetDamageRadius(200)
		self.Launcher1.SetDamageHealth(25)
		self.Launcher1.SetRelativeDamage(False)
		self.Launcher1.SetAutomaticMoveRotate(False)

		self.Launcher2 = self.CreateProjectileLauncher(shared.LauncherManager.UNITLAUNCHER)
		self.Launcher2.SetPosition(0, 40, 15)
		self.Launcher2.SetRotation(0, 0, 0)
		self.Launcher2.SetProjectile("rocket")
		self.Launcher2.SetFireRange(700)
		self.Launcher2.SetFiringSpeed(2)
		self.Launcher2.SetFiringDelay(0.1)
		self.Launcher2.SetReloadingSpeed(5)
		self.Launcher2.SetMagasineCapasity(-1)
		self.Launcher2.CanReloadLive(True)
		self.Launcher2.SetDamageRadius(200)
		self.Launcher2.SetDamageHealth(25)
		self.Launcher2.SetRelativeDamage(False)
		self.Launcher2.SetAutomaticMoveRotate(False)

		self.Launcher3 = self.CreateProjectileLauncher(shared.LauncherManager.UNITLAUNCHER)
		self.Launcher3.SetPosition(10, 35, 12)
		self.Launcher3.SetRotation(0, 0, 0)
		self.Launcher3.SetProjectile("rocket")
		self.Launcher3.SetFireRange(700)
		self.Launcher3.SetFiringSpeed(2)
		self.Launcher3.SetFiringDelay(0.2)
		self.Launcher3.SetReloadingSpeed(5)
		self.Launcher3.SetMagasineCapasity(-1)
		self.Launcher3.CanReloadLive(True)
		self.Launcher3.SetDamageRadius(200)
		self.Launcher3.SetDamageHealth(25)
		self.Launcher3.SetRelativeDamage(False)
		self.Launcher3.SetAutomaticMoveRotate(False)

	def OnCreation(self, pos):
		th = shared.Map.Terrain.getHeightAtPos(pos[0], pos[2])
		self.SetPosition(pos[0], th, pos[2])
		self.SetupProjectileLaunchers()

	# Action Triggers

	def OnPrimaryAction(self, unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def PrimaryFire(self, unit):
		self.Launcher1.FireAtUnit(unit)
		self.Launcher2.FireAtUnit(unit)
		self.Launcher3.FireAtUnit(unit)