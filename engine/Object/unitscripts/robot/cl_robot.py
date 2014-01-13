#Tank - Ground Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit
from engine.Object.unitact import cl_construct
from ogre.renderer.OGRE import Degree

class Unit(BaseUnit):
	Name = "Robot"
	Description = "Type: Ground Infantry / Worker\nEffective against Infantry, Airunits\nCan build structures"
	Image = "unit_robot"
	Buildtime = 3
	Cost = 150

	def Initialize(self, ID):
		self.SetEntity("robot")
		self.SetSelectedText("Infantry "+str(self.GetID()))
		self.Actions=[cl_construct.generate("build")]

		self.dead=False

		self.Hook.Add("OnCreation", self.OnCreation)
		self.Hook.Add("OnDeath", self.OnDie)
		self.Hook.Add("OnThink", self.OnThink)
		self.Hook.Add("OnMove", self.OnMove)
		self.Hook.Add("OnMoveStop", self.OnIdle)

	def OnCreation(self, pos):
		self.GetEntity().actNone()

	def OnDie(self, cause):
		self.GetEntity().actNone()
		self.GetEntity().actDead(True)
		self.dead=True
		return True

	def OnThink(self, delta):
		if self.dead:
			if self.GetEntity().getIfAnimIsFinish():
				self.Destroy()

	def OnMove(self, pos):
		self.GetEntity().actMove(True)

	def OnIdle(self, pos):
		self._randomCallback(10, 50, self.RandomIdleAnim)
		self.GetEntity().actNone()

	def RandomIdleAnim(self): #Custom callback defined in OnIdle
		if self.GetState()=="Idle":
			self.GetEntity().actIdle(True)

	#Action Triggers
	def OnPrimaryAction(self, unit):
		self.GetEntity().actAnim(0, True)

	def OnPrimaryActionAbort(self):
		self.GetEntity().actNone()

	def OnPrimaryActionFinish(self):
		self.GetEntity().actNone()

	def AimAtUnit(self, unit):
		x, y, z = unit.GetEntity().GetPosition()
		self.GetEntity().LookAtZ(x, y, z)
		self._entity.node.yaw(Degree(float(30)))

	#Hackish overwrite of basefunction _look as the robot mesh is rotated wrong
	def _look(self, pos):
		if len(pos) == 3:
			self._entity.LookAtZ(pos[0], pos[1], pos[2])
		else:
			self._entity.LookAtZ(pos[0], self._getPosition()[1], pos[1])
		self._entity.node.yaw(Degree(float(270)))