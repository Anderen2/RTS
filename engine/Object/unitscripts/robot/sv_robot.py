#Robot - Ground Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit
from engine.Object.unitact import sv_construct

#AddCSFile("cl_init.py")

class Unit(BaseUnit):
	Name = "Robot"
	Description = "Type: Ground Infantry / Worker\nEffective against Infantry, Airunits\nCan build structures"
	Image = "unit_robot"
	Buildtime = 3
	Cost = 150

	def Initialize(self, ID):
		self.SetEntity("robot")
		self.SetSolid(True)

		self.Actions=[sv_construct.generate("build"), sv_construct.generate("turret"), sv_construct.generate("power")]

		self.SetMoveType(1) #MOVETYPE_GROUND
		self.SetMoveSpeed(50)
		self.SetHealth(20)
		self.SetViewRange(100)

		self.SetVehicleMaxForce(0.5)
		self.SetVehicleMass(1)
		self.SetVehiclePathNodeRadius(30)
		self.SetVehicleArriveBreakingRadius(30)
		self.SetVehicleMaxVelocity(1)
		self.SetVehicleMaxSpeed(1)
		self.SetVehicleBreakingForce(0.1)
		self.SetVehicleSize(2)
		self.SetVehicleMaxSeeAhead(50)
		self.SetVehicleMaxAvoidForce(10)

		self.Hook.Add("OnCreation", self.OnCreation)

	def SetupProjectileLaunchers(self):
		self.Launcher1 = self.CreateProjectileLauncher(shared.LauncherManager.UNITLAUNCHER)
		self.Launcher1.SetPosition(10, 10, 0)
		self.Launcher1.SetRotation(0, 0, 0)
		self.Launcher1.SetProjectile("bullet")
		self.Launcher1.SetFireRange(250)
		self.Launcher1.SetFiringSpeed(0.5)
		self.Launcher1.SetReloadingSpeed(2)
		self.Launcher1.SetMagasineCapasity(25)
		self.Launcher1.CanReloadLive(True)
		self.Launcher1.SetDamageRadius(0)
		self.Launcher1.SetDamageHealth(5)
		self.Launcher1.SetRelativeDamage(False)
		self.Launcher1.SetAutomaticMoveRotate(True)

	def OnCreation(self, pos):
		self.SetupProjectileLaunchers()
		th = shared.Map.Terrain.getHeightAtPos(pos[0], pos[2])
		self.SetPosition(pos[0], th, pos[2])

	#Action Triggers
	def OnPrimaryAction(self, unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def PrimaryFire(self, unit):
		self.Launcher1.FireAtUnit(unit)