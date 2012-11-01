#Render3dExtension - render3dwater
#Classes for rendering water
#Lowlevel module

from engine import shared, debug
from engine.shared import DPrint
import ogre.renderer.OGRE as ogre

class WaterManager():
	def __init__(self):
		self.wcount=0

	def Create(self, Pos, Height, Width):
		self.wcount=self.wcount+1
		return Water(self.wcount,Pos, Height, Width)

class Water():
	def __init__(self, ID, Pos, Height, Width):
		plane=ogre.Plane((0,1,0),0)
		MeshManager=ogre.MeshManager.getSingleton()
		MeshManager.createPlane("Water", "General", plane, Height, Width, 100, 100, True, 1, 100, 100, (0,0,1))
		self.Entity=shared.render3dScene.sceneManager.createEntity("Water"+str(ID),"Water")
		self.Entity.setMaterialName("OceanHLSL_GLSL")
		self.Entity.setCastShadows(False)
		self.Entity.setRenderQueueGroup(ogre.RENDER_QUEUE_SKIES_LATE)
		self.node=shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode()
		self.node.attachObject(self.Entity)
		self.node.setPosition(Pos)

	def __del__(self):
		pass