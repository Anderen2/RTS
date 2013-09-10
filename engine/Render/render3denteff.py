#Render3dEnt Extension - render3denteff
#Classes for handeling Entity "Effects"

from engine import shared, debug
from engine.shared import DPrint
from engine.shared import Vector
from twisted.internet import reactor

class BuildEffect():
	def __init__(self, ent):
		self.ent = ent

	def Start(self):
		reactor.callLater(0, self.AABBShit)
		debug.ACC("be_progress", self.UpdateProgress, info="Change build progress of the last structure", args=1)

	def AABBShit(self):
		self.meshname = self.ent.params["mesh"]
		
		#Create new mesh at the buildsite
		self.buildmesh = shared.render3dScene.sceneManager.createEntity(self.meshname)
		self.buildmesh.setCastShadows(False)
		self.buildnode = shared.render3dScene.sceneManager.getSceneNode("EntNode").createChildSceneNode()
		self.buildnode.attachObject(self.buildmesh)
		self.buildnode.scale(self.ent.params["meshscale"][0],self.ent.params["meshscale"][1],self.ent.params["meshscale"][2])

		#Position according to terrain
		self.entpos = self.ent.node.getPosition()
		self.terrainheight = shared.render3dTerrain.getHeightAtPos(self.entpos.x, self.entpos.z)
		self.YOffset=self.ent.mesh.getWorldBoundingBox().getHalfSize().y
		print("YOffset")
		print(self.YOffset)
		self.buildnode.setPosition(self.entpos.x, self.terrainheight+self.YOffset, self.entpos.z)

		#Use an material to color it transparent green
		self.buildmesh.setMaterialName("RTS/BuildHolo")

		#Position self.ent directly below ground
		self.ent.node.setPosition(self.entpos.x, self.terrainheight-self.YOffset, self.entpos.z)

		#Calculate progress-step according to entity height
		self.progstep = (self.YOffset*2) / 100

	def UpdateProgress(self, progress):
		#Update progress/position according to progstep, entity height and terrain height
		progress = float(progress)
		self.ent.node.setPosition(self.entpos.x, (self.terrainheight-self.YOffset)+(self.progstep*progress), self.entpos.z)