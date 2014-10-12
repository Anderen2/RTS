#Build - Unit Structure
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit
from engine.Object.unitact import sv_setway, sv_settarg, sv_unitbuild, sv_const

#AddCSFile("cl_init.py")

class Unit(BaseUnit):
	UnitID = "build"
	Name = "House"
	Description = "Type: Military-grade multifactory disguised as an house\nCreates: All Unittypes"
	Image = "unit_house"
	Buildtime = 10
	Cost = 1500

	def Initialize(self, ID):
		self.SetEntity("command")
		self.SetSolid(True)

		self.Actions=[sv_unitbuild.generate("mig"), sv_unitbuild.generate("tank"), sv_unitbuild.generate("robot")]

		self.SetMoveType(-1) #MOVETYPE_NONE
		self.SetMoveSpeed(0)
		self.SetMaxHealth(1000)
		self.SetViewRange(500)

		self.Destination = None

		#Overwrite GlobalActions [This should be changed for an less hackishlike solution]
		self._globalactions = [sv_setway.Action, sv_settarg.Action, sv_const.Action]
		self.Hook.Add("OnCreation", self.OnCreation)

	def OnCreation(self, pos):
		th = shared.Map.Terrain.getHeightAtPos(pos[0], pos[2])
		self.SetPosition(pos[0], th, pos[2])