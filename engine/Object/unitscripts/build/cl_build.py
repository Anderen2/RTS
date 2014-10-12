#Build - Unit Structure
#Clientside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit
from engine.Object.unitact import cl_setway, cl_settarg, cl_unitbuild, cl_const
from engine.Render import render3denteff

class Unit(BaseUnit):
	UnitID = "build"
	Name = "House"
	Description = "Type: Military-grade multifactory disguised as an house\nCreates: All Unittypes"
	Image = "unit_house"
	BuildEntity = "command"
	Buildtime = 10
	Cost = 1500

	def Initialize(self, ID):
		self.SetEntity("command")
		self.SetSelectedText("BuildStructure: "+str(self.GetID()))
		self.Actions=[cl_unitbuild.generate("mig"), cl_unitbuild.generate("tank"), cl_unitbuild.generate("robot")]
		print(self.Actions[0].actionid)

		self.Destination = None

		#Overwrite GlobalActions [This should be changed for an less hackishlike solution]
		self._globalactions = [cl_setway.Action, cl_settarg.Action, cl_const.Action]

		self.Hook.Add("OnDeath", self.OnDie)
		self.Hook.Add("OnCreation", self.StartBuild)
		self.Hook.Add("OnServerUpdate", self.AttributesUpdated)

	def OnDie(self, cause):
		self.GetPosition()
		shared.EffectManager.Create("explosion", self._pos[0], self._pos[1], self._pos[2], 1, 1)

	def StartBuild(self, pos):
		pass
		#self.buildeffect = render3denteff.BuildEffect(self.GetEntity())
		#self.buildeffect.Start()

	def AttributesUpdated(self, attibs):
		self.buildeffect.UpdateProgress(0)