#Power - Unit Structure
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit
from engine.Object.unitact import sv_setway, sv_settarg, sv_unitbuild, sv_const

#AddCSFile("cl_init.py")

class Unit(BaseUnit):
	Name = "Power"
	Description = "Power Structure\nGives your base power"
	Image = "unit_power"
	BuildEntity = "power"
	Buildtime = 4
	Cost = 800

	def Initialize(self, ID):
		self.SetEntity("power")
		self.SetSolid(True)

		self.Actions=[]

		self.SetMoveType(-1) #MOVETYPE_NONE
		self.SetMoveSpeed(0)
		self.SetMaxHealth(200)
		self.SetViewRange(200)

		self.Destination = None

		#Overwrite GlobalActions [This should be changed for an less hackishlike solution]
		self._globalactions = [sv_setway.Action, sv_settarg.Action, sv_const.Action]
		self.Hook.Add("OnCreation", self.OnCreation)

	def OnCreation(self, pos):
		th = shared.Map.Terrain.getHeightAtPos(pos[0], pos[2])
		self.SetPosition(pos[0], th, pos[2])