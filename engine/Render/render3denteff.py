#Render3dEnt Extension - render3denteff
#Classes for handeling Entity "Effects"

from engine import shared, debug
from engine.shared import DPrint
from engine.shared import Vector
from twisted.internet import reactor

MASK_OTHER = 1 << 3 #All other entitys

class BuildEffect():
	def __init__(self, ent):
		self.ent = ent
		self.entpos = None

	def Start(self):
		reactor.callLater(0, self.AABBShit) #Need to wait one frame for the AABB-model to update correctly before continuing
		debug.ACC("be_progress", self.UpdateProgress, info="Change build progress of the last structure", args=1)

	def AABBShit(self):
		self.meshname = self.ent.params["mesh"]
		
		#Create new mesh at the buildsite
		self.buildmesh = shared.render3dScene.sceneManager.createEntity(self.meshname)
		self.buildmesh.setCastShadows(False)
		self.buildmesh.setQueryFlags(MASK_OTHER)
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
		print(progress)
		if self.entpos!=None:
			print("I am not none!")
			progress = float(progress)
			self.ent.node.setPosition(self.entpos.x, (self.terrainheight-self.YOffset)+(self.progstep*progress), self.entpos.z)

	def Remove(self):
		self.buildnode.detachObject(self.buildmesh)
		shared.render3dScene.sceneManager.destroyEntity(self.buildmesh.getName())
		shared.render3dScene.sceneManager.destroySceneNode(self.buildnode.getName())

class BuildEffect2():
	def __init__(self, entname, pos):
		self.entname = entname
		self.entpos = pos

	def Start(self):
		debug.ACC("be_progress", self.UpdateProgress, info="Change build progress of the last structure", args=1)

		self.entparams = shared.EntityHandeler.GetParams(self.entname)
		self.meshname = self.entparams["mesh"]

		self.ent = shared.render3dScene.sceneManager.createEntity(self.meshname)
		self.ent.setCastShadows(False)
		self.entnode = shared.render3dScene.sceneManager.getSceneNode("EntNode").createChildSceneNode()
		self.entnode.attachObject(self.ent)
		self.entnode.scale(self.entparams["meshscale"][0],self.entparams["meshscale"][1],self.entparams["meshscale"][2])

	def AABBShit(self):		
		#Create new mesh at the buildsite
		self.buildmesh = shared.render3dScene.sceneManager.createEntity(self.meshname)
		self.buildmesh.setCastShadows(False)
		self.buildnode = shared.render3dScene.sceneManager.getSceneNode("EntNode").createChildSceneNode()
		self.buildnode.attachObject(self.buildmesh)
		self.buildnode.scale(self.entparams["meshscale"][0],self.entparams["meshscale"][1],self.entparams["meshscale"][2])

		#Use an material to color it transparent green
		self.buildmesh.setMaterialName("RTS/BuildHolo")

		#Position according to terrain
		self.terrainheight = shared.render3dTerrain.getHeightAtPos(self.entpos.x, self.entpos.z)
		self.YOffset=self.ent.getWorldBoundingBox().getHalfSize().y
		print("YOffset")
		print(self.YOffset)
		self.buildnode.setPosition(self.entpos.x, self.terrainheight+self.YOffset, self.entpos.z)

		#Position self.ent directly below ground
		self.entnode.setPosition(self.entpos.x, self.terrainheight-self.YOffset, self.entpos.z)

		#Calculate progress-step according to entity height
		self.progstep = (self.YOffset*2) / 100

	def UpdateProgress(self, progress):
		#Update progress/position according to progstep, entity height and terrain height
		progress = float(progress)
		self.entnode.setPosition(self.entpos.x, (self.terrainheight-self.YOffset)+(self.progstep*progress), self.entpos.z)

class PlacementEffect():
	def __init__(self, entname, callback):
		self.entname = entname
		self.callback = callback

	def Start(self):
		self.entparams = shared.EntityHandeler.GetParams(self.entname)
		self.meshname = self.entparams["mesh"]

		#Create new mesh at the buildsite
		self.buildmesh = shared.render3dScene.sceneManager.createEntity(self.meshname)
		self.buildmesh.setCastShadows(False)
		self.buildnode = shared.render3dScene.sceneManager.getSceneNode("EntNode").createChildSceneNode()
		self.buildnode.attachObject(self.buildmesh)
		self.buildnode.scale(self.entparams["meshscale"][0],self.entparams["meshscale"][1],self.entparams["meshscale"][2])

		#Add nessesary renderio hooks
		shared.renderioInput.Hook.Add("OnMouseMove", self.MouseMove)
		shared.renderioInput.Hook.Add("OnMousePressed", self.MouseRelease)

		self.YOffset=self.buildmesh.getWorldBoundingBox().getHalfSize().y
		reactor.callLater(0, self.AABBShit) #Reupdate the YOffset after one frame

		#Use an material to color it transparent green
		self.buildmesh.setMaterialName("RTS/BuildHolo")

		#Calculate progress-step according to entity height
		self.progstep = (self.YOffset*2) / 100

	def AABBShit(self):
		self.YOffset=self.buildmesh.getWorldBoundingBox().getHalfSize().y

	def MouseMove(self, pos):
		worldpos = shared.render3dSelectStuff.mousePosToWorldTerrainPos()
		#terrainheight = shared.render3dTerrain.getHeightAtPos(worldpos.x, worldpos.z)
		self.buildnode.setPosition(worldpos[0], worldpos[1]+self.YOffset, worldpos[2])

	def MouseRelease(self, mkey, pos):
		print("KEY:")
		print(mkey)
		print(repr(mkey))
		print(str(mkey))

		shared.renderioInput.Hook.RM("OnMouseMove", self.MouseMove)
		shared.renderioInput.Hook.RM("OnMousePressed", self.MouseRelease)

		self.buildnode.detachObject(self.buildmesh)
		shared.render3dScene.sceneManager.destroyEntity(self.buildmesh.getName())
		shared.render3dScene.sceneManager.destroySceneNode(self.buildnode.getName())

		if str(mkey)=="MB_Left":
			self.callback(shared.render3dSelectStuff.mousePosToWorldTerrainPos())

		