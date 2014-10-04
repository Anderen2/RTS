#render3deffects

from engine import shared, debug
from random import randrange
import ogre.renderer.OGRE as ogre
from twisted.internet import reactor

class EffectManager():
	def __init__(self):
		self.types={"explosion":Explosion, "smallexplosion":SmallExplosion, "atomic":Atomic, "rain":Rain, "snow":Snow}
		self.effects=[]
		self.count=0
		debug.ACC("eff_create", self.Create, info="Create effect\nusage: type x y z size time", args=6)

	def Create(self, effect, x, y, z, size, time):
		eff=self.types[effect](self.count, (float(x), float(y), float(z)), float(size), float(time))
		self.effects.append(eff)
		self.count+=1

class Explosion():
	def __init__(self, ID, position, size, time):
		self.ID = ID
		self.particle=shared.render3dScene.sceneManager.createParticleSystem("expeff"+str(self.ID),"Explosion")
		self.node = shared.render3dScene.sceneManager.getSceneNode("EffNode").createChildSceneNode("expeff"+str(self.ID))

		self.node.setPosition(position)
		self.node.attachObject(self.particle)
		self.node.setScale(size, size, size)
		self.particle.getEmitter(0).setTimeToLive(time)
		self.particle.getEmitter(0).setEnabled(True)

		reactor.callLater(10, self.Stop)

	def Stop(self):
		for x in range(0, self.particle.getNumEmitters()):
			self.particle.getEmitter(x).setEnabled(False)

		reactor.callLater(5, self.Remove)

	def Remove(self):
		shared.EffectManager.effects.remove(self)

	def __del__(self):
		self.node.detachObject(self.particle)
		shared.render3dScene.sceneManager.destroyParticleSystem(self.particle)
		shared.render3dScene.sceneManager.destroySceneNode(self.node)

class SmallExplosion():
	def __init__(self, ID, position, size, time):
		self.ID = ID
		self.particle=shared.render3dScene.sceneManager.createParticleSystem("expeff"+str(self.ID),"SmallExplosion")
		self.node = shared.render3dScene.sceneManager.getSceneNode("EffNode").createChildSceneNode("expeff"+str(self.ID))

		self.node.setPosition(position)
		self.node.attachObject(self.particle)
		self.node.setScale(size, size, size)
		self.particle.getEmitter(0).setTimeToLive(time)
		self.particle.getEmitter(0).setEnabled(True)

		reactor.callLater(10, self.Stop)

	def Stop(self):
		for x in range(0, self.particle.getNumEmitters()):
			self.particle.getEmitter(x).setEnabled(False)

		reactor.callLater(5, self.Remove)

	def Remove(self):
		shared.EffectManager.effects.remove(self)

	def __del__(self):
		self.node.detachObject(self.particle)
		shared.render3dScene.sceneManager.destroyParticleSystem(self.particle)
		shared.render3dScene.sceneManager.destroySceneNode(self.node)

class Atomic():
	def __init__(self, ID, position, size, time):
		self.ID = ID
		self.particle=shared.render3dScene.sceneManager.createParticleSystem("expeff"+str(self.ID),"Atomic")
		self.node = shared.render3dScene.sceneManager.getSceneNode("EffNode").createChildSceneNode("expeff"+str(self.ID))

		self.node.setPosition(position)
		self.node.setScale(size, size, size)
		self.node.attachObject(self.particle)
		for x in range(0, self.particle.getNumEmitters()):
			self.particle.getEmitter(x).setEnabled(True)

		reactor.callLater(time, self.Stop)

	def Stop(self):
		for x in range(0, self.particle.getNumEmitters()):
			self.particle.getEmitter(x).setEnabled(False)
		
		reactor.callLater(5, self.Remove)

	def Remove(self):
		shared.EffectManager.effects.remove(self)
		self.node.detachObject(self.particle)
		shared.render3dScene.sceneManager.destroyParticleSystem(self.particle)
		shared.render3dScene.sceneManager.destroySceneNode(self.node)

class Rain():
	def __init__(self, ID, position, size, time):
		self.ID = ID
		self.particle=shared.render3dScene.sceneManager.createParticleSystem("expeff"+str(self.ID),"Rain")
		self.node = shared.render3dCamera.pitchnode.createChildSceneNode("expeff"+str(self.ID))
		self.node.setInheritOrientation(False)

		#self.node.setPosition(position)
		#self.node.setPosition()
		#shared.render3dCamera.camNode.attachObject(self.node)
		self.node.setScale(size, size, size)
		self.node.attachObject(self.particle)
		for x in range(0, self.particle.getNumEmitters()):
			#print(x)
			#self.particle.getEmitter(0).setTimeToLive(time)
			self.particle.getEmitter(x).setEnabled(True)

		#reactor.callLater(time, self.Stop)

	def Stop(self):
		for x in range(0, self.particle.getNumEmitters()):
			self.particle.getEmitter(x).setEnabled(False)
		
		reactor.callLater(5, self.Remove)

	def Remove(self):
		shared.EffectManager.effects.remove(self)
		self.node.detachObject(self.particle)
		shared.render3dScene.sceneManager.destroyParticleSystem(self.particle)
		shared.render3dScene.sceneManager.destroySceneNode(self.node)

class Snow():
	def __init__(self, ID, position, size, time):
		self.ID = ID
		self.particle=shared.render3dScene.sceneManager.createParticleSystem("expeff"+str(self.ID),"Snow")
		self.node = shared.render3dCamera.pitchnode.createChildSceneNode("expeff"+str(self.ID))
		self.node.setInheritOrientation(False)

		#self.node.setPosition(position)
		self.node.setScale(size, size, size)
		self.node.attachObject(self.particle)
		print("Let it snow")
		for x in range(0, self.particle.getNumEmitters()):
			#print(x)
			#self.particle.getEmitter(0).setTimeToLive(time)
			self.particle.getEmitter(x).setEnabled(True)

		#reactor.callLater(time, self.Stop)

	def Stop(self):
		print("Stop")
		for x in range(0, self.particle.getNumEmitters()):
			self.particle.getEmitter(x).setEnabled(False)
		
		reactor.callLater(5, self.Remove)

	def Remove(self):
		print("Remove")
		shared.EffectManager.effects.remove(self)
		self.node.detachObject(self.particle)
		shared.render3dScene.sceneManager.destroyParticleSystem(self.particle)
		shared.render3dScene.sceneManager.destroySceneNode(self.node)