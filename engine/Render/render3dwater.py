#Render3dExtension - render3dwater
#Classes for rendering water
#Lowlevel module

from engine import shared, debug
from engine.shared import DPrint
import ogre.renderer.OGRE as ogre

MASK_WATER = 1 << 6

class WaterManager():
	def __init__(self):
		self.wcount=0
		self.waters=[]

	def Create(self, Pos, Height, Width):
		self.wcount=self.wcount+1
		water=Water(self.wcount, Pos, Height, Width)
		self.waters.append(water)
		return water

	def CreateUno(self, Altitude):
		self.wcount=self.wcount+1

		# terrainLength=
		# terrainHeight=

		water=Water(self.wcount, Pos, Height, Width)
		self.waters.append(water)
		return water

	def Remove(self, ID):
		self.waters[ID].destroy()
		del self.waters[ID]

def ConsoleFriendly(X, Y, Z, L, H):
	shared.WaterManager.Create((float(X),float(Y),float(Z)),float(L),float(H))

debug.ACC("water", ConsoleFriendly, args=5, info="Create a waterplane. \nUsage: water X Y Z Length Width")

class Water():
	def __init__(self, ID, Pos, Length, Width):
		plane=ogre.Plane((0,1,0),0)
		MeshManager=ogre.MeshManager.getSingleton()
		MeshManager.createPlane("Water"+str(ID), "General", plane, Width, Length, 100, 100, True, 1, 100, 100, (0,0,1))
		self.Entity=shared.render3dScene.sceneManager.createEntity("Water"+str(ID),"Water"+str(ID))
		self.Entity.setMaterialName("OceanHLSL_GLSL")
		self.Entity.setCastShadows(False)
		#self.Entity.setRenderQueueGroup(ogre.RENDER_QUEUE_SKIES_LATE)
		self.Entity.setQueryFlags(MASK_WATER)
		self.node=shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode()
		self.node.attachObject(self.Entity)
		self.node.setPosition(Pos)

	def destroy(self):
		self.node.detachObject(self.Entity)
		shared.render3dScene.sceneManager.destroyEntity(self.Entity.getName())
		shared.render3dScene.sceneManager.destroySceneNode(self.node.getName())

	def __del__(self):
		pass