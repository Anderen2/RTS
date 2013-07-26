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
		self.SetMoveSpeed(1)
		self.SetHealth(100)
		self.SetViewRange(200)

		#self.SetupProjectileLaunchers()

	def SetupProjectileLaunchers(self):
		self.Launcher1 = self.CreateProjectileLauncher()
		self.Launcher1.SetPosition(10, 10, 10)
		self.Launcher1.SetRotation(10, 10, 10)
		self.Launcher1.SetProjectile("rocket")
		self.Launcher1.SetFireRange(100)
		self.Launcher1.SetFiringSpeed(1)
		self.Launcher1.SetReloadingSpeed(2)
		self.Launcher1.SetMagasineCapasity(10)
		self.Launcher1.CanReloadLive(True) #Can this unit reload while in air/movement? Or does it have to stop or reload at a buildning

		self.Launcher2 = self.CreateProjectileLauncher()
		self.Launcher2.SetPosition(30, 30, 30)
		self.Launcher2.SetRotation(30, 30, 30)
		self.Launcher2.SetProjectile("rocket")
		self.Launcher2.SetFireRange(100)
		self.Launcher2.SetFiringSpeed(1)
		self.Launcher2.SetReloadingSpeed(2)
		self.Launcher2.SetMagasineCapasity(10)
		self.Launcher2.CanReloadLive(True) #Can this unit reload while in air/movement? Or does it have to stop or reload at a buildning

	def OnCreation(self, pos):
		pass

	def OnDie(self):
		pass

	def OnThink(self, delta):
		pass

	def OnPrimaryAction(self, unit):
		if unit.GetTeam()!=self.GetTeam():
			if self.IsFreeSightTo(unit): 
				if self.GetFireRange>self.GetDistanceTo(unit):
					self.Launcher1.FireAtUnit(unit)
					self.Launcher2.FireAtUnit(unit)

	def OnMove(self, pos):
		pass

	def Act1(self, data):
		#This is an dummy action, but it should cover the networking part of additional actions
		if "unit" in data:
			print("Doing some action on a unit!")
			print(data["unit"])

		if "ground" in data:
			print("Havin' some action on the ground")
			print(data["pos"])