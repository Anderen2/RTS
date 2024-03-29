#MIG - Air Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit
import sv_act

#AddCSFile("cl_init.py")

class Unit(BaseUnit):
	UnitID = "mig"
	Name = "MIG"
	Description = "Type: Air Fighter\nEffective against Airunits, Armored Units"
	Image = "unit_mig"
	Buildtime = 5
	Cost = 750

	def Initialize(self, ID):
		self.Actions=[sv_act.Action]

		self.setAttributeInitial("entity.name","plane")
		self.setAttributeInitial("entity.solid", True)
		self.setAttributeInitial("movement.movetype", 0)
		self.setAttributeInitial("movement.movespeed", 100)
		self.setAttributeInitial("movement.constantaltitude", 200)
		self.setAttributeInitial("unit.health", 100)
		self.setAttributeInitial("unit.viewrange", 500)
		self.setAttributeInitial("vehicle.size", 10)
		self.setAttributeInitial("vehicle.max_force", 2)
		self.setAttributeInitial("vehicle.mass", 200)
		self.setAttributeInitial("vehicle.path_node_radius", 100)
		self.setAttributeInitial("vehicle.arrive_breaking_radius", 50)
		self.setAttributeInitial("vehicle.max_velocity", 3)
		self.setAttributeInitial("vehicle.max_speed", 2)
		self.setAttributeInitial("vehicle.breaking_force", 1)
		self.setAttributeInitial("vehicle.max_see_ahead", 50)
		self.setAttributeInitial("vehicle.max_avoid_force", 10)

		self.Hook.Add("OnCreation", self.OnCreation)

	def SetupProjectileLaunchers(self):
		self.Launcher1 = self.CreateProjectileLauncher(shared.LauncherManager.UNITLAUNCHER)
		self.Launcher1.SetPosition(0, 0, -20)
		self.Launcher1.SetRotation(10, 10, 10)
		self.Launcher1.SetProjectile("rocket")
		self.Launcher1.SetFireRange(400)
		self.Launcher1.SetFiringSpeed(2)
		self.Launcher1.SetReloadingSpeed(5)
		self.Launcher1.SetMagasineCapasity(5)
		self.Launcher1.CanReloadLive(True)
		self.Launcher1.SetDamageRadius(150)
		self.Launcher1.SetDamageHealth(10)
		self.Launcher1.SetRelativeDamage(False)
		self.Launcher1.SetAutomaticMoveRotate(True)

		self.Launcher2 = self.CreateProjectileLauncher(shared.LauncherManager.UNITLAUNCHER)
		self.Launcher2.SetPosition(0, 0, 20)
		self.Launcher2.SetRotation(30, 30, 30)
		self.Launcher2.SetProjectile("rocket")
		self.Launcher2.SetFireRange(400)
		self.Launcher2.SetFiringSpeed(2)
		self.Launcher2.SetReloadingSpeed(5)
		self.Launcher2.SetMagasineCapasity(5)
		self.Launcher2.CanReloadLive(True)
		self.Launcher2.SetDamageRadius(150)
		self.Launcher2.SetDamageHealth(10)
		self.Launcher2.SetRelativeDamage(False)
		self.Launcher2.SetAutomaticMoveRotate(True)

	def OnCreation(self, pos):
		self.SetupProjectileLaunchers()
		self.SetPosition(pos[0], pos[1], pos[2])

	#Action Triggers
	def OnPrimaryAction(self, unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def PrimaryFire(self, unit):
		self.Launcher1.FireAtUnit(unit)
		self.Launcher2.FireAtUnit(unit)