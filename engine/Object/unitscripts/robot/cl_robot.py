#Tank - Ground Unit
#Serverside Unit Script File

from engine import shared, debug
from engine.Object.unitscripts.cl_baseunit import BaseUnit
from engine.Object.unitact import cl_construct
from ogre.renderer.OGRE import Degree

class Unit(BaseUnit):
	UnitID = "robot"
	Name = "Robot"
	Description = "Type: Ground Infantry / Worker\nEffective against Infantry, Airunits\nCan build structures"
	Image = "unit_robot"
	BuildEntity = "robot"
	Buildtime = 3
	Cost = 150

	def Initialize(self, ID):
		self.SetEntity("robot")
		self.SetSelectedText("Infantry "+str(self.GetID()))
		self.Actions=[cl_construct.generate("build"), cl_construct.generate("turret"), cl_construct.generate("power"), cl_construct.generate("derrick")]

		self.dead=False
		self.hackOnTheMove=True

		self.Hook.Add("OnCreation", self.OnCreation)
		self.Hook.Add("OnDeath", self.OnDie)
		self.Hook.Add("OnThink", self.OnThink)
		self.Hook.Add("OnMove", self.OnMove)
		self.Hook.Add("OnMoving", self.OnMoving)
		self.Hook.Add("OnMoveStop", self.OnIdle)
		#self._vehicle.Hook.Add("OnPathEnd", self.OnIdle)

	def OnCreation(self, pos):
		self.GetEntity().actNone()

	def OnDie(self, cause):
		self.GetEntity().actNone()
		self.GetEntity().actDead(True)
		self.dead=True
		shared.DPrint("UnitRobot", 0, "OnDie..")
		return True

	def OnThink(self, delta):
		if self.dead:
			print("I am Dead")
			if self.GetEntity().getIfAnimIsFinish():
				#self.dead = None
				self.Destroy()

	def OnMoving(self):
		if not self.dead:
			if self.hackOnTheMove:
				self._entity.node.yaw(Degree(float(270))) #Hackish override as the model is rotated wrong

	def OnMove(self, pos):
		if not self.dead:
			self.hackOnTheMove=True
			self.GetEntity().actMove(True)

	def OnIdle(self, pos):
		if not self.dead:
			self.hackOnTheMove=False
			#self._randomCallback(10, 50, self.RandomIdleAnim)
			self.GetEntity().actNone()

	def RandomIdleAnim(self): #Custom callback defined in OnIdle
		if not self.hackOnTheMove:
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