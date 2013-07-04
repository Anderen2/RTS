#Projectiles

from engine import shared, debug
from random import randrange
from twisted.internet import reactor

class BaseProjectile():
	def __init__(self):
		pass

class Rocket(BaseProjectile):
	def __init__(self, pos):
		self.ID=randrange(0,9999,1)
		self.team=0
		self.entity=shared.EntityHandeler.Create(self.ID, "rocket", "proj", self.team)
		self.entity.SetPosition(pos[0], pos[1], pos[2])
		self.entity.CreateTextOverlay()
		self.entity.text.setText("dist: 10 - TTI: 5")

		self.target=None

	def ignite(self, pos):
		print("Firing at "+str(pos))
		self.target=pos
		self.entity.actMove(True)

	def _think_(self):
		if self.target!=None:
			if type(self.target) is tuple:
				if self._step_(self.target[0], self.target[1], self.target[2])<2:
					self.target=None
					self._explode_()
			if self.target == False:
				return False

		return True

	def _step_(self, x, y, z):
		src=self.entity.node.getPosition()
		src3d=(src[0], src[1], src[2]) #2D Coordinates (X, Z) or Longitude and Latitude (Not Altitude!)
		xzd=shared.Pathfinder.ABPath.GetNextCoord3D(src3d, (x,y,z)) #Returns next Xcoord, Zcoord and a measure of how much distance which is left (x, z, dist)

		self.entity.LookAtZ(self.target[0], self.target[1], self.target[2])
		self.entity.SetPosition(xzd[0], xzd[1], xzd[2])
		self.entity.RPYRotate(0, 90, 0)
		return xzd[3]

	def _explode_(self):
		print("Exploded.")
		pos=self.entity.node.getPosition()
		src3d=(pos[0], pos[1], pos[2])
		shared.EffectManager.Create("explosion", pos[0], pos[1], pos[2], 1, 2)
		reactor.callLater(5, self.blown)
		self.entity.actNone()
		self.entity.Delete()
		self.target=True

	def blown(self):
		self.target=False

	def __del__(self):
		shared.DPrint("Projectiles",5,"Projectile deleted: "+str(self.ID))

		# try:
		# 	xExsist=None
		# 	for x in shared.render3dSelectStuff.CurrentSelection:
		# 		if self.entity.node.getName() == x.getName():
		# 			xExsist=x
		# 	if xExsist!=None:
		# 		shared.render3dSelectStuff.CurrentSelection.remove(xExsist)

		# 	if not entity.error:
		# 		self.entity.Delete()

		# except:
		# 	shared.DPrint("Projectiles",5,"Projectile Deletion Failed! Projectile may still be in memory and/or in game world!")

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