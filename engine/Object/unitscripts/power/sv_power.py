#Power - Unit Structure
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit
from engine.Object.unitact import sv_setway, sv_settarg, sv_unitbuild, sv_const

import sv_upgrade
#AddCSFile("cl_init.py")

class Unit(BaseUnit):
	UnitID = "power"
	Name = "Power"
	Description = "Power Structure\nGives your base power"
	Image = "unit_power"
	BuildEntity = "power"
	Buildtime = 4
	Cost = 800

	def Initialize(self, ID):
		self.Actions=[sv_upgrade.Action]

		self.setAttributeInitial("entity.name", "power")
		self.setAttributeInitial("entity.solid", True)
		self.setAttributeInitial("movement.movetype", -1)
		self.setAttributeInitial("movement.movespeed", 0)
		self.setAttributeInitial("unit.health", 200)
		self.setAttributeInitial("unit.viewrange", 200)

		self.Destination = None

		#Overwrite GlobalActions [This should be changed for an less hackishlike solution]
		self._globalactions = [sv_setway.Action, sv_settarg.Action, sv_const.Action]
		self.Hook.Add("OnCreation", self.OnCreation)

	def OnCreation(self, pos):
		th = shared.Map.Terrain.getHeightAtPos(pos[0], pos[2])
		self.SetPosition(pos[0], th, pos[2])