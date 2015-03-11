#Tank - Ground Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit

#AddCSFile("cl_init.py")

class Unit(BaseUnit):
	UnitID = "tank"
	Name = "Tank"
	Description = "Type: Ground Armored Vehicle\nEffective against Infantry, Armored Units"
	Image = "unit_tank"
	Buildtime = 6
	Cost = 500

	def Initialize(self, ID):
		self.Actions=[]

		self.setAttributeInitial("entity.name", "tank")
		self.setAttributeInitial("entity.solid", True)
		self.setAttributeInitial("movement.movetype", 1)
		self.setAttributeInitial("movement.movespeed", 50)
		self.setAttributeInitial("unit.health", 350)
		self.setAttributeInitial("unit.viewrange", 400)
		self.setAttributeInitial("unit.autoengage", False)
		self.setAttributeInitial("vehicle.size", 10)
		self.setAttributeInitial("vehicle.max_force", 1)
		self.setAttributeInitial("vehicle.mass", 10)
		self.setAttributeInitial("vehicle.path_node_radius", 50)
		self.setAttributeInitial("vehicle.arrive_breaking_radius", 50)
		self.setAttributeInitial("vehicle.max_velocity", 2.5)
		self.setAttributeInitial("vehicle.max_speed", 1.5)
		self.setAttributeInitial("vehicle.breaking_force", 0.8)
		self.setAttributeInitial("vehicle.max_see_ahead", 50)
		self.setAttributeInitial("vehicle.max_avoid_force", 10)

		self.Hook.Add("OnCreation", self.OnCreation)

	def SetupProjectileLaunchers(self):
		self.Launcher1 = self.CreateProjectileLauncher(shared.LauncherManager.UNITLAUNCHER)
		self.Launcher1.SetPosition(10, 10, 0)
		self.Launcher1.SetRotation(0, 0, 0)
		self.Launcher1.SetProjectile("shell")
		self.Launcher1.SetFireRange(350)
		self.Launcher1.SetFiringSpeed(2)
		self.Launcher1.SetReloadingSpeed(5)
		self.Launcher1.SetMagasineCapasity(1)
		self.Launcher1.CanReloadLive(True)
		self.Launcher1.SetDamageRadius(200)
		self.Launcher1.SetDamageHealth(50)
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