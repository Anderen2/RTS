#Clientside Projectiles/Launchers

from time import time
from twisted.internet import reactor
from engine.Object import projectiles
from engine import shared, debug

class ProjectileManager():
	def __init__(self):
		shared.ProjectileManager=self
		shared.objectManager.addEntry(0, 6, self)
		self.Projectiles={}

		self.lastframe=time()
		self.update()

	def recv_rocket(self, uid, pos, target, speed, Protocol=None):
		projectile = projectiles.Rocket(uid, pos, target, speed)
		self.Projectiles[uid] = projectile
		projectile.ignite(target)

	def recv_explode(self, uid, pos, Protocol=None):
		for ID, projectile in self.Projectiles.iteritems():
			if uid == ID:
				projectile._explode(pos)

	def update(self):
		deltatime = time()-self.lastframe
		self.lastframe=time()

		for uid, projectile in self.Projectiles.iteritems():
			projectile._think(deltatime)
		reactor.callLater(0, self.update)
