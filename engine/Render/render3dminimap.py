#Render3dExtension - render3dminimap
#Classes for rendering and managing the minimap
#Lowlevel Module

import ogre.renderer.OGRE as ogre
import ogre.gui.CEGUI as CEGUI
import math
from engine import shared, debug
from engine.World import posalgo
from engine.Render.render3dshapes import Path, RemoveMesh
from traceback import print_exc

class MinimapListener(ogre.RenderTargetListener,ogre.Node.Listener):
	def __init__(self):
		ogre.RenderTargetListener.__init__(self)
		ogre.Node.Listener.__init__(self)

		self.created=False

		self.UnitIndicators=[]
		self.WarningIndicators=[]

		debug.ACC("dbg_minimap", self.debugmode, info="Enable minimap viewPort", args=0)
		debug.ACC("mm_warn", self.createWarn, info="Simulate a warning", args=3)

	def Create(self, tsizex, tsizey, textureTarget):
		shared.DPrint("render3dminimap", 0, "Creating Minimap RTT")
		self.created = True
		self.tsizex = 5000
		self.tsizey = 5000
		self.tsize = (tsizex+tsizey) / 2
		self.camAlt = 0 #Find out an algorithm to calculate this properly (HARDCODE)

		# shared.render3dScene.sceneManager
		self.sceneManager = ogre.Root.getSingleton().createSceneManager(ogre.ST_EXTERIOR_CLOSE)
		self.sceneManager.setAmbientLight(ogre.ColourValue(1,1,1))

		#Setup camera
		self.camera = self.sceneManager.createCamera("minimapCam")
		self.camera.setAspectRatio(1)
		self.camNode = self.sceneManager.getRootSceneNode().createChildSceneNode()
		self.camNode.attachObject(self.camera)
		self.camera.setProjectionType(ogre.PT_ORTHOGRAPHIC)
		self.camera.setOrthoWindowHeight(self.tsizex)
		self.camera.setOrthoWindowWidth(self.tsizey)
		self.camNode.setPosition(self.tsizex/2, 200, self.tsizey/2)
		self.camera.lookAt((self.tsizex/2)+0.01, 1, self.tsizey/2)

		#Create material for the terrain layout
		self.planeMat = ogre.MaterialManager.getSingleton().create("MinimapTexture",ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME)

		planeTex = self.planeMat.getTechnique(0).getPass(0).createTextureUnitState("minimap3.png")

		#Create plane showing terrain layout
		self.plane = ogre.MovablePlane("MinimapPlane")
		self.plane.d = 0
		self.plane.normal = ogre.Vector3().UNIT_Y
		self.planeMesh = ogre.MeshManager.getSingleton().createPlane("MinimapPlane", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME, self.plane, self.tsizex, self.tsizey, 1, 1, True, 1, 1, 1, ogre.Vector3().UNIT_Z)
		self.planeMesh.getSubMesh(0).setMaterialName("MinimapTexture")
		self.planeEnt = self.sceneManager.createEntity("Plane", "MinimapPlane")
		self.planeNode = self.sceneManager.getRootSceneNode().createChildSceneNode()
		self.planeNode.attachObject(self.planeEnt)
		self.planeNode.setPosition(self.tsizex/2, 0, self.tsizey/2)
		self.planeNode.yaw(ogre.Radian(ogre.Degree(180)))


		#Pass for applying texture to planeMat
		self.planePass = self.planeMat.getTechnique(0).createPass()
		self.planePass.setSceneBlending(ogre.SBT_MODULATE)

		self.FOWtex = self.planePass.createTextureUnitState("RttTex") 
		self.FOWtex.setProjectiveTexturing(True, shared.FowManager.camera) # allow the texture to be updated via projections from FOWcamera
		self.FOWtex.setTextureAddressingMode(ogre.TextureUnitState.TAM_CLAMP) # when color values go above 1.0, they are set to 1.0 

		#Create RTT for CEGUI
		ogre.TextureManager.getSingleton().setDefaultNumMipmaps(0)
		self.texture = ogre.TextureManager.getSingleton().createManual( "MinimapRTT", "General", ogre.TextureType.TEX_TYPE_2D, 300, 300, 1, ogre.MIP_DEFAULT, ogre.PixelFormat.PF_R8G8B8, ogre.TU_RENDERTARGET | ogre.TU_AUTOMIPMAP | ogre.TU_STATIC )

		#Render Target
		self.FOWTarget = self.texture.getBuffer().getRenderTarget()
		self.FOWTarget.addViewport(self.camera)
		self.FOWTarget.getViewport(0).setOverlaysEnabled(False)
		self.FOWTarget.getViewport(0).setClearEveryFrame(True)
		self.FOWTarget.getViewport(0).clear()
		self.FOWTarget.getViewport(0).setBackgroundColour(ogre.ColourValue().Black)

		self.FOWTarget.update()

		#Hook into FOW and steal its rendering
		shared.FowManager.renderTargets.append(self.FOWTarget)

		#Create cegui texture
		self.ceguiTexture = CEGUI.System.getSingleton().getRenderer().createTexture(self.texture)
		shared.gui['minimap'].Initialize()

		self.InitializeUnitIndicators()
		self.MinimapCameraIndicator = MinimapCameraIndicator()

		self.InitializeWarningIndicators()

		# test = self.createUnitIndicator(6, (0, 1, 0))
		# test[1].setPosition(3000,1, 2000)

		# test2= self.createUnitIndicator(6, (1, 0, 0))
		# test2[1].setPosition(2500, 1, 2500)

		# test3= self.createUnitIndicator(6, (0, 0, 1))
		# test3[1].setPosition(1500, 1, 1500)

		# test4= self.createUnitIndicator(6, (0, 0, 1))
		# test4[1].setPosition(1700, 1, 1700)

	def InitializeUnitIndicators(self):
		UnitIndicator = ogre.MovablePlane("UnitIndicator")
		UnitIndicator.d = 0
		UnitIndicator.normal = ogre.Vector3().UNIT_Y

		self.UnitIndicatorMat = ogre.MaterialManager.getSingleton().create("MM_UnitIndicator", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME)
		#UnitIndicatorMat.setDiffuse(1,0,0,1)
		# UnitIndicatorMat.setAmbient(1,1,1)
		self.UnitIndicatorMat.getTechnique(0).getPass(0).createTextureUnitState("minimapDot2.png")
		#UnitIndicatorMat.setSelfIllumination(1,0,0)
		self.UnitIndicatorMat.setSceneBlending(ogre.SBT_TRANSPARENT_ALPHA)
		self.UnitIndicatorMat.setDepthWriteEnabled(False)

		UnitIndicatorMesh = ogre.MeshManager.getSingleton().createPlane("MM_UnitIndicator", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME, UnitIndicator, 16, 16, 1, 1, True, 1, 1, 1, ogre.Vector3().UNIT_Z)
		UnitIndicatorMesh.getSubMesh(0).setMaterialName("MM_UnitIndicator")

	def InitializeWarningIndicators(self):
		WarningIndicator = ogre.MovablePlane("WarningIndicator")
		WarningIndicator.d = 0
		WarningIndicator.normal = ogre.Vector3().UNIT_Y

		self.WarningIndicatorMat = ogre.MaterialManager.getSingleton().create("MM_WarningIndicator", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME)
		self.WarningIndicatorMat.getTechnique(0).getPass(0).createTextureUnitState("warn1.png")
		self.WarningIndicatorMat.setSceneBlending(ogre.SBT_TRANSPARENT_ALPHA)
		self.WarningIndicatorMat.setDepthWriteEnabled(False)

		WarningIndicatorMesh = ogre.MeshManager.getSingleton().createPlane("MM_WarningIndicator", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME, WarningIndicator, 65, 60, 1, 1, True, 1, 1, 1, ogre.Vector3().UNIT_Z)
		WarningIndicatorMesh.getSubMesh(0).setMaterialName("MM_WarningIndicator")

		shared.render.Hook.Add("OnRenderFrame", self.update)

	def updateUnitIndicators(self, node=None):
		pass

	def newUnitIndicator(self):
		UI = MinimapUnitIndicator()
		return UI

	def debugmode(self):
		debug.RCC("gui_hideall")
		self.viewPort = shared.render.root.getAutoCreatedWindow().addViewport(self.camera, 1, 0, 0.5, 0.2, 0.2)

	def createWarn(self, x, z, warnlvl):
		foo = MinimapWarningIndicator()
		foo.Node.setPosition(int(x), 1, int(z))
		foo.setWarnLvl(int(warnlvl))


	def update(self, delta):
		for WarningIndicator in self.WarningIndicators:
			WarningIndicator.frame(delta)


class MinimapUnitIndicator():
	def __init__(self):
		self.size = 6
		self.color = (1,1,1)
		self.unit = None
		self.selectable = False

		self.Entity = shared.MinimapManager.sceneManager.createEntity("UI"+str(len(shared.MinimapManager.UnitIndicators)), "MM_UnitIndicator")
		self.Entity.setCastShadows(False)

		self.Material = shared.MinimapManager.UnitIndicatorMat.clone("MM_UI"+str(len(shared.MinimapManager.UnitIndicators)))
		self.Material.setAmbient(self.color[0],self.color[1],self.color[2])

		#Entity.getMesh().getSubMesh(0).setMaterialName("MM_UI"+str(len(self.UIEnts)))
		self.Entity.setMaterial(self.Material)


		self.Node = shared.MinimapManager.sceneManager.getRootSceneNode().createChildSceneNode()
		self.Node.attachObject(self.Entity)
		self.Node.setPosition(2000, 1, 1000)
		self.Node.setScale(1*self.size, 1*self.size, 1*self.size)
		self.Node.showBoundingBox(False)

		shared.MinimapManager.UnitIndicators.append(self)

	def setUnit(self, unit):
		if self.unit!=None:
			shared.DPrint("render3dminimap", 0, "UnitIndicator changed owner!")

		self.unit = unit
		unit._unitIndicator = self
		self.update()

	def setColor(self, color):
		self.color = color
		self.Material.setAmbient(float(color[0])/255, float(color[1])/255, float(color[2])/255)

	def setSize(self, size):
		self.size = size
		self.Node.setScale(1*self.size, 1*self.size, 1*self.size)

	def setVisible(self, visible):
		self.visible = visible
		self.Node.setVisible(visible)

	def remove(self):
		self.Node.detachObject(self.Entity)
		shared.MinimapManager.sceneManager.destroyEntity(self.Entity)
		if self.unit!=None:
			self.unit._unitIndicator = None
		shared.MinimapManager.UnitIndicators.remove(self)

	def update(self):
		if self.unit:
			self.Node.setPosition(self.unit._pos[0], 1, self.unit._pos[2])
			self.setColor(self.unit._owner.color)
			self.selectable = self.unit._owner.yourself
			self.setVisible(self.unit._visible)


class MinimapWarningIndicator():
	def __init__(self):
		self.size = 6
		self.color = (255,0,0)
		self.unit = None
		self.selectable = False
		self.jaw=0
		self.warnlevels = {0: (255,255,255), 1: (0, 255, 0), 2: (0, 0, 255), 3: (255,255,0), 4:(255,0,0)}

		self.Entity = shared.MinimapManager.sceneManager.createEntity("WI"+str(len(shared.MinimapManager.WarningIndicators)), "MM_WarningIndicator")
		self.Entity.setCastShadows(False)

		self.Material = shared.MinimapManager.WarningIndicatorMat.clone("WI_UI"+str(len(shared.MinimapManager.WarningIndicators)))
		self.Material.setAmbient(self.color[0],self.color[1],self.color[2])

		#Entity.getMesh().getSubMesh(0).setMaterialName("MM_UI"+str(len(self.UIEnts)))
		self.Entity.setMaterial(self.Material)


		self.Node = shared.MinimapManager.sceneManager.getRootSceneNode().createChildSceneNode()
		self.Node.attachObject(self.Entity)
		self.Node.setPosition(2000, 1, 1000)
		self.Node.setScale(1*self.size, 1*self.size, 1*self.size)
		self.Node.showBoundingBox(False)

		self.setColor(self.color)

		shared.MinimapManager.WarningIndicators.append(self)

	def setWarnLvl(self, warnlvl):
		#0 = Information
		#1 = Friendly
		#2 = Friendly 2
		#3 = Attention
		#4 = Warning
		self.setColor(self.warnlevels[warnlvl])


	def setUnit(self, unit):
		if self.unit!=None:
			shared.DPrint("render3dminimap", 0, "WarningIndicator changed owner!")

		self.unit = unit
		unit._unitIndicator = self
		self.update()

	def setColor(self, color):
		self.color = color
		self.Material.setAmbient(float(color[0])/255, float(color[1])/255, float(color[2])/255)

	def setSize(self, size):
		self.size = size
		self.Node.setScale(1*self.size, 1*self.size, 1*self.size)

	def setVisible(self, visible):
		self.visible = visible
		self.Node.setVisible(visible)

	def remove(self):
		self.Node.detachObject(self.Entity)
		shared.MinimapManager.sceneManager.destroyEntity(self.Entity)
		if self.unit!=None:
			self.unit._unitIndicator = None
		shared.MinimapManager.WarningIndicators.remove(self)

	def update(self):
		if self.unit:
			self.Node.setPosition(self.unit._pos[0], 1, self.unit._pos[2])
			self.setColor(self.unit._owner.color)
			self.selectable = self.unit._owner.yourself
			self.setVisible(self.unit._visible)

	def frame(self, delta):
		# self.jaw+=0.0001
		# if self.jaw>359:
		# 	self.jaw = 0
		self.Node.yaw(0.05)
	

class MinimapCameraIndicator():
	def __init__(self):
		self.Mesh=None
		self.regenerateMesh()

		shared.render3dCamera.Hook.Add("OnMove", self.update)
		shared.render3dCamera.Hook.Add("OnSetPos", self.updateAbs)
		shared.renderioInput.Hook.Add("OnKeyReleased", self.regenerateHook)

		debug.ACC("mm_cireg", self.regenerateMesh, info="Regenerate camera indicator mesh")

	def regenerateMesh(self):
		screenCorners = [shared.render3dSelectStuff.RelScreenPosToWorldTerrainPos(0,0), shared.render3dSelectStuff.RelScreenPosToWorldTerrainPos(0,1), shared.render3dSelectStuff.RelScreenPosToWorldTerrainPos(1,1), shared.render3dSelectStuff.RelScreenPosToWorldTerrainPos(1,0)]
		screenCorners = [(screenCorners[0][0],1,screenCorners[0][2]), (screenCorners[1][0],1,screenCorners[1][2]), (screenCorners[2][0],1,screenCorners[2][2]), (screenCorners[3][0],1,screenCorners[3][2]), (screenCorners[0][0],1,screenCorners[0][2])]
		print(screenCorners)
		if self.Mesh!=None:
			#RemoveMesh(self.Mesh)
			print("Detaching")
			self.Node.detachObject(self.Mesh)
			shared.MinimapManager.sceneManager.destroyManualObject(self.Mesh)
			#shared.MinimapManager.FOWTarget.getViewport(0).clear()
			#shared.MinimapManager.sceneManager.destroyEntity(self.Entity)

		self.Mesh = Path("MinimapCameraIndicator", "BaseWhiteNoLighting", screenCorners)
		#self.Entity = shared.MinimapManager.sceneManager.createEntity(self.Mesh, "MinimapCameraIndicator")
		self.Node = shared.MinimapManager.sceneManager.getRootSceneNode().createChildSceneNode()
		self.Node.attachObject(self.Mesh)
		#self.Node.setPosition(shared.render3dCamera.pitchnode.getPosition())
		#self.Node.setScale(2,2,2)
		#self.Node.setPosition(150, 1, 150)
	
	def update(self, direction):
		self.Node.translate(direction)

	def updateAbs(self, pos, prev):
		p1v = shared.Vector3D((pos[0], 1, pos[1]))
		p2v = shared.Vector3D((prev[0], 1, prev[1]))

		trans = p1v - p2v

		#self.Node.setPosition(pos[0], 1, pos[1])
		self.Node.translate(trans[0], 1, trans[2])
		#self.regenerateMesh()

	def regenerateHook(self, key):
		if key == shared.renderioInput.keys["camstear"] or key == shared.renderioInput.keys["up"] or key == shared.renderioInput.keys["down"]:
			self.regenerateMesh()