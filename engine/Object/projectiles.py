#Projectiles

from engine import shared, debug
from random import randrange
from twisted.internet import reactor

class BaseProjectile():
	def __init__(self):
		pass

class Rocket(BaseProjectile):
	def __init__(self, uid, pos, target, speed):
		self.uid=uid
		self.target = None
		self.speed = speed
		self.team=0

		self.entity=shared.EntityHandeler.Create(self.uid, "rocket", "proj", self.team)
		self.entity.SetPosition(pos[0], pos[1], pos[2])
		self.entity.CreateTextOverlay()
		self.entity.text.setText("dist: 0 - TTI: 0")

	def ignite(self, target):
		print("Firing at "+str(target))
		self.target=target
		self.entity.actMove(True)

	def _think(self, delta):
		if self.target!=None:
			if type(self.target) is tuple:
				dist = self._movestep(self.target, delta)
				self.UpdateText(dist)
				if dist<1:
					self.target=None

	def _movestep(self, dst, delta):
		src = self.GetPosition()
		speed = (self.speed*delta)
		nx, ny, nz, dist = shared.Pathfinder.ABPath.GetNextCoord3D(src, dst, speed)
		newpos = (nx, ny, nz)
		
		self.SetPosition(newpos)
		return dist

	def _explode(self, pos):
		print("Exploded.")
		#pos=self.entity.node.getPosition()
		shared.EffectManager.Create("explosion", pos[0], pos[1], pos[2], 1, 2)

		self.entity.actNone()
		self.entity.Delete()

		reactor.callLater(5, self._blown)
		
		self.target=None

	def _blown(self):
		pass

	def UpdateText(self, dist):
		TTI = dist/self.speed
		self.entity.text.setText("dist: "+str(dist)+" - TTI: "+str(TTI))
		self.entity.text.update()

	def SetPosition(self, pos):
		self.entity.node.setPosition(pos[0], pos[1], pos[2])

	def GetPosition(self):
		pos = self.entity.node.getPosition()
		return (pos.x, pos.y, pos.z)

	def __del__(self):
		shared.DPrint("Projectiles",5,"Projectile deleted: "+str(self.ID))

class DummyLauncher():
	def __init__(self):
		self.Projectiles=[]
		reactor.callLater(1, self.update)
		debug.ACC("fire", self.Fire, info="Fire a rocket at pos \n usage: fire 10 10 10", args=3)

	def Fire(self, x, y, z):
		proj=Rocket((0, 500, 0))
		self.Projectiles.append(proj)
		proj.ignite((int(x), int(y), int(z)))

	def update(self):
		for x in self.Projectiles:
			x._think_()
		reactor.callLater(0, self.update)