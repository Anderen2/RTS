#Build - Unit Structure
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.sv_baseunit import BaseUnit
from engine.Object.unitact import sv_setway, sv_settarg
from engine.Object.unitscripts.build import sv_mig

#AddCSFile("cl_init.py")

class Unit(BaseUnit):
	def Initialize(self):
		self.Name = "build"
		self.SetEntity("house")
		self.SetSolid(True)

		self.Actions=[sv_mig.Action]

		self.SetMoveType(-1)
		self.SetMoveSpeed(0)
		self.SetHealth(1000)
		self.SetViewRange(500)

		self.Destination = None

		#Overwrite GlobalActions [This should be changed for an less hackishlike solution]
		self._globalactions = [sv_setway.Action, sv_settarg.Action]

	def OnCreation(self, pos):
		th = shared.Map.Terrain.getHeightAtPos(pos[0], pos[2])
		self.SetPosition(pos[0], th+50, pos[2])

	def OnDie(self):
		pass

	def OnThink(self, delta):
		pass

	def OnPrimaryAction(self, unit):
		pass

	def OnPrimaryActionAbort(self):
		pass

	def OnPrimaryActionFinish(self):
		pass

	def PrimaryFire(self, unit):
		pass

	def OnMove(self, pos):
		pass