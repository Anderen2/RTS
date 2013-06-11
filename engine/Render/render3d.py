#Rendermodule - render3d
#Classes for rendering 3d enviroment
#By Anderen2 (Dec. 2012)

import render3dent, render3ddecal, render3dwaypoint, render3dwater, render3dcamera, render3dfow, render3dselection
from engine import shared, debug
import ogre.renderer.OGRE as ogre
from ogre.gui.CEGUI import MouseCursor
from random import randrange
from string import split
from math import floor
from traceback import print_exc
from twisted.internet import reactor

class Scene():
	def __init__(self):
		self.root=shared.renderRoot
		self.TerrainMaterial=None

	def Setup(self):
		shared.DPrint("Render3d",1,"Scenemanager..")
		self.sceneManager = self.root.createSceneManager(ogre.ST_EXTERIOR_CLOSE, "Default sceneManager")
		shared.DPrint("Render3dScene",1,"Current scenemanager: %s" % str(self.sceneManager.getTypeName()))

		shared.DPrint("Render3d",1,"Terrain..")
		
		if self.TerrainMaterial==None:
			self.createTerrainMaterial("2048.png", {"terr_rock-dirt.jpg":"alphamap.png", "grass_1024.jpg":"alphamap2.png"})

		self.sceneManager.setWorldGeometry ("terrain.cfg")

		shared.DPrint("Render3d",1,"Skybox..")
		self.sceneManager.setSkyBox (True, "Examples/SpaceSkyBox")

		shared.DPrint("Render3d",1,"Camera..")
		shared.render3dCamera=render3dcamera.Camera(self.root, self)
		self.camera=shared.render3dCamera

		shared.DPrint("Render3d",1,"Particle Parameters")
		ogre.ParticleSystem.defaultNonVisibleUpdateTimeout=1

		shared.DPrint("Render3d",1,"Selection..")
		shared.render3dSelectStuff=render3dselection.SelectStuff(self.root, self)

		shared.DPrint("Render3d",1,"EntityHandeler..")
		self.EntNode=self.sceneManager.getRootSceneNode().createChildSceneNode("EntNode",(0,0,0))
		self.StatNode=self.sceneManager.getRootSceneNode().createChildSceneNode("StatNode",(0,0,0))
		shared.EntityHandeler=render3dent.EntityHandeler()
		shared.DPrint("Render3d",1,"	Loading entitys..")
		shared.EntityHandeler.ReadEntitys()
		shared.DPrint("Render3d",1,"	Entitys successfuly loaded!")

		shared.DPrint("Render3d",1,"DecalManager...")
		shared.DecalManager=render3ddecal.DecalManager()
		shared.DPrint("Render3d",1,"	Defining decals..")
		shared.DecalManager.Declare()
		shared.DPrint("Render3d",1,"	Decals successfuly declared!")

		shared.DPrint("Render3d",1,"WaypointManager..")
		shared.WaypointManager=render3dwaypoint.WaypointManager()
		shared.DPrint("Render3d",1,"	Loading Waypoints..")
		shared.WaypointManager.Load()

		shared.DPrint("Render3d",1,"WaterManager..")
		shared.WaterManager=render3dwater.WaterManager()

		debug.ACC("r_pfenable", self.PostFilterEnable, info="Enable a postfilter", args=1)
		debug.ACC("r_pfdisable", self.PostFilterDisable, info="Disable a postfilter", args=1)
		debug.ACC("r_pm", self.PolygenMode, info="Change the polygenmode. 1 for points, 2 for wireframe, 3 for solid", args=1)
		debug.ACC("r_aabb", self.cAABB, info="View all bounding boxes, 1/0", args=1)
		debug.ACC("r_reloadterrain", self.RldTerrain, info="Reload the terrain", args=0)

	def cAABB(self, onoff):
		if onoff==str(1):
			self.sceneManager.showBoundingBoxes(True)
		else:
			self.sceneManager.showBoundingBoxes(False)

	def RldTerrain(self):
		try:
			self.sceneManager.setWorldGeometry("terrain2.cfg")
		except:
			print_exc()

	def FowSetup(self):
		shared.DPrint("Render3d",1,"New FOWManager..")
		#self, terrain, tsizex, tsizey, tsize)
		shared.FowManager=render3dfow.FogOfWarListener("Template/Terrain", 1500, 1500, 1500)
		shared.FowManager.Create()

	def createTerrainMaterial(self, base, splatting):
		if self.TerrainMaterial!=None:
			self.TerrainMaterial.removeAllTechniques()
			Technique=self.TerrainMaterial.createTechnique()
			basePass=Technique.createPass()
		else:
			self.TerrainMaterial = ogre.MaterialManager.getSingleton().create("Template/Terrain",ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME) 

		Technique=self.TerrainMaterial.getTechnique(0)
		basePass=Technique.getPass(0)
		baseTexture = basePass.createTextureUnitState()
		baseTexture.setTextureName(base)
		baseTexture.setTextureScale(1, 1)

		for texture, alphamap in splatting.iteritems():
			splattingPass = Technique.createPass()
			splattingPass.setLightingEnabled(False)
			splattingPass.setSceneBlending(ogre.SBT_TRANSPARENT_ALPHA)
			splattingPass.setDepthFunction(ogre.CMPF_EQUAL)

			alphamapTexture = splattingPass.createTextureUnitState()
			alphamapTexture.setTextureName(alphamap)
			alphamapTexture.setAlphaOperation(ogre.LBX_SOURCE1, ogre.LBS_TEXTURE, ogre.LBS_TEXTURE)
			alphamapTexture.setColourOperationEx(ogre.LBX_SOURCE2, ogre.LBS_TEXTURE, ogre.LBS_TEXTURE)

			detailTexture = splattingPass.createTextureUnitState()
			detailTexture.setTextureName(texture)
			detailTexture.setTextureScale(0.07, 0.07)
			detailTexture.setColourOperationEx(ogre.LBX_BLEND_DIFFUSE_ALPHA, ogre.LBS_TEXTURE, ogre.LBS_CURRENT)

		# lightingPass = Technique.createPass()
		# lightingPass.setAmbient(1,1,1)
		# lightingPass.setDiffuse(1,1,1,0)
		# lightingPass.setDepthFunction(ogre.CMPF_EQUAL)
		# lightingPass.setSceneBlending(ogre.SBF_ZERO, ogre.SBF_ONE_MINUS_SOURCE_COLOUR )

	def PostFilterEnable(self,PF):
		ogre.CompositorManager.getSingleton().addCompositor(shared.render3dCamera.viewPort, PF)
		ogre.CompositorManager.getSingleton().setCompositorEnabled(shared.render3dCamera.viewPort, PF, True)

	def PostFilterDisable(self,PF):
		ogre.CompositorManager.getSingleton().setCompositorEnabled(shared.render3dCamera.viewPort, PF, False)

	def PolygenMode(self, PM):
		PM=int(PM)
		if PM==1:
			shared.render3dCamera.camera.setPolygonMode(ogre.PM_POINTS)
		elif PM==2:
			shared.render3dCamera.camera.setPolygonMode(ogre.PM_WIREFRAME)
		else:
			shared.render3dCamera.camera.setPolygonMode(ogre.PM_SOLID)

