#Tank - Ground Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit

#AddCSFile("cl_init.py")

class Unit(BaseUnit):

	def Initialize(self, ID):
		self.Name = "tank"
		self.SetEntity("tank")
		self.SetSolid(True)

		self.Actions=[]

		self.SetMoveType(1) #MOVETYPE_GROUND
		self.SetMoveSpeed(50)
		self.SetHealth(200)
		self.SetViewRange(200)

		self.Hook.Add("OnCreation", self.OnCreation)

	def SetupProjectileLaunchers(self):
		self.Launcher1 = self.CreateProjectileLauncher(shared.LauncherManager.UNITLAUNCHER)
		self.Launcher1.SetPosition(10, 10, 0)
		self.Launcher1.SetRotation(0, 0, 0)
		self.Launcher1.SetProjectile("shell")
		self.Launcher1.SetFireRange(500)
		self.Launcher1.SetFiringSpeed(2)
		self.Launcher1.SetReloadingSpeed(5)
		self.Launcher1.SetMagasineCapasity(1)
		self.Launcher1.CanReloadLive(True)
		self.Launcher1.SetDamageRadius(200)
		self.Launcher1.SetDamageHealth(25)
		self.Launcher1.SetRelativeDamage(False)
		self.Launcher1.SetAutomaticMoveRotate(True)

	def OnCreation(self, pos):
		self.SetupProjectileLaunchers()
		th = shared.Map.Terrain.getHeightAtPos(pos[0], pos[2])
		self.SetPosition(pos[0], th, pos[2])

	# Action Triggers

	def OnPrimaryAction(self, unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def PrimaryFire(self, unit):
		self.Launcher1.FireAtUnit(unit)