#Rendermodule - render3d
#Classes for rendering 3d enviroment
#By Anderen2 (Dec. 2012)

import render3dent, render3deffects, render3ddecal, render3dterrain, render3dwaypoint, render3dwater, render3dcamera, render3dfow, render3dselection, render3ddebug
from engine.Object import projectiles
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

	def Setup(self):
		#mTerrainGlobals = ogre.Terrain()
		#print mTerrainGlobals
		shared.DPrint("Render3d",1,"Scenemanager..")
		self.sceneManager = self.root.createSceneManager(ogre.ST_EXTERIOR_CLOSE, "Default sceneManager")
		shared.DPrint("Render3dScene",1,"Current scenemanager: %s" % str(self.sceneManager.getTypeName()))

		shared.DPrint("Render3d",1,"Light...")
		self.sceneManager.ambientLight = (1,1,1)
		sunlight = self.sceneManager.createLight("DirectionalLight")
		sunlight.type = ogre.Light.LT_DIRECTIONAL
		sunlight.diffuseColour = (.5,.5,.0)
		sunlight.specularColour = (.75,.75,.75)
		sunlight.direction = (0,-1,-1)

		shared.DPrint("Render3d",1,"Terrain..")
		shared.render3dTerrain = render3dterrain.Terrain(self.sceneManager)

		shared.DPrint("Render3d",1,"Skybox..")
		self.sceneManager.setSkyBox (True, "Examples/SpaceSkyBox")

		shared.DPrint("Render3d",1,"Camera..")
		shared.render3dCamera=render3dcamera.Camera(self.root, self)
		self.camera=shared.render3dCamera

		shared.DPrint("Render3d",1,"Particle Parameters")
		ogre.ParticleSystem.defaultNonVisibleUpdateTimeout=1

		shared.DPrint("Render3d",1,"Effects..")
		self.EffNode=self.sceneManager.getRootSceneNode().createChildSceneNode("EffNode",(0,0,0))
		shared.EffectManager=render3deffects.EffectManager()

		shared.DPrint("Render3d",1,"DummyLauncher..")
		shared.DummyLauncher = projectiles.DummyLauncher()

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

		shared.DPrint("Render3d",1,"Debugtools..")
		shared.RenderDebug=render3ddebug.aStarView()		

		debug.ACC("r_pfenable", self.PostFilterEnable, info="Enable a postfilter", args=1)
		debug.ACC("r_pfdisable", self.PostFilterDisable, info="Disable a postfilter", args=1)
		debug.ACC("r_pm", self.PolygenMode, info="Change the polygenmode. 1 for points, 2 for wireframe, 3 for solid", args=1)
		debug.ACC("r_aabb", self.cAABB, info="View all bounding boxes, 1/0", args=1)

	def cAABB(self, onoff):
		if onoff==str(1):
			self.sceneManager.showBoundingBoxes(True)
		else:
			self.sceneManager.showBoundingBoxes(False)

	def FowSetup(self):
		shared.DPrint("Render3d",1,"New FOWManager..")
		shared.FowManager=render3dfow.FogOfWarListener()

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

