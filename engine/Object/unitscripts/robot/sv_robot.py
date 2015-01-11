#Robot - Ground Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit
from engine.Object.unitact import sv_construct

#AddCSFile("cl_init.py")

class Unit(BaseUnit):
	UnitID = "robot"
	Name = "Robot"
	Description = "Type: Ground Infantry / Worker\nEffective against Infantry, Airunits\nCan build structures"
	Image = "unit_robot"
	Buildtime = 3
	Cost = 150

	def Initialize(self, ID):
		self.Actions=[sv_construct.generate("build"), sv_construct.generate("turret"), sv_construct.generate("power"), sv_construct.generate("derrick")]

		self.setAttributeInitial("entity.name", "robot")
		self.setAttributeInitial("entity.solid", True)
		self.setAttributeInitial("movement.movetype", 1)
		self.setAttributeInitial("movement.movespeed", 50)
		self.setAttributeInitial("unit.health", 50)
		self.setAttributeInitial("unit.viewrange", 350)
		self.setAttributeInitial("vehicle.size", 2)
		self.setAttributeInitial("vehicle.max_force", 0.5)
		self.setAttributeInitial("vehicle.mass", 1)
		self.setAttributeInitial("vehicle.path_node_radius", 30)
		self.setAttributeInitial("vehicle.arrive_breaking_radius", 30)
		self.setAttributeInitial("vehicle.max_velocity", 1)
		self.setAttributeInitial("vehicle.max_speed", 1)
		self.setAttributeInitial("vehicle.breaking_force", 0.01)
		self.setAttributeInitial("vehicle.max_see_ahead", 50)
		self.setAttributeInitial("vehicle.max_avoid_force", 10)

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