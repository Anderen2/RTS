#Render3dExtension - render3dminimap
#Classes for rendering and managing the minimap
#Lowlevel Module

import ogre.renderer.OGRE as ogre
import math
from engine import shared, debug
from engine.World import posalgo
from traceback import print_exc

class MinimapListener(ogre.RenderTargetListener,ogre.Node.Listener):
	def __init__(self):
		ogre.RenderTargetListener.__init__(self)
		ogre.Node.Listener.__init__(self)

		self.created=False


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
		#TUS = self.planeMat.getTechnique(0).getPass(0).createTextureUnitState("RttTex")
		#TUS.setProjectiveTexturing(True, shared.FowManager.camera)

		planeTex = self.planeMat.getTechnique(0).getPass(0).createTextureUnitState("minimap3.png")
		print("\n------------------------------------------------------------")
		#print(str(planeTex.getTextureDimensions()))
		#self.planeMat.setSceneBlending(ogre.SBT_REPLACE )
		#self.planeMat.setDepthWriteEnabled(False)

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

		# Setup RTT for FOW
		ogre.TextureManager.getSingleton().setDefaultNumMipmaps(0)
		self.texture = ogre.TextureManager.getSingleton().createManual( "MinimapRTT", "General", ogre.TextureType.TEX_TYPE_2D, 300, 300, 1, 1, ogre.PixelFormat.PF_R8G8B8, ogre.TU_RENDERTARGET )
		#self.RT = self.texture.getBuffer().getRenderTarget()

		#Pass for applying texture to planeMat
		self.planePass = self.planeMat.getTechnique(0).createPass()
		self.planePass.setSceneBlending(ogre.SBT_MODULATE)

		self.FOWtex = self.planePass.createTextureUnitState("RttTex") 

		# !!
		self.FOWtex.setProjectiveTexturing(True, shared.FowManager.camera) # allow the texture to be updated via projections from FOWcamera
		self.FOWtex.setTextureAddressingMode(ogre.TextureUnitState.TAM_CLAMP) # when color values go above 1.0, they are set to 1.0 
		# self.FOWtex.setTextureScale(0.5, 0.5)

		# #print(str(FOWtex.getTextureDimensions()))

		#FOW RTT
		self.FOWTarget = self.texture.getBuffer().getRenderTarget()
		self.FOWTarget.addViewport(shared.FowManager.camera)
		self.FOWTarget.getViewport(0).setOverlaysEnabled(False)
		self.FOWTarget.getViewport(0).setClearEveryFrame(False)
		self.FOWTarget.getViewport(0).clear()
		self.FOWTarget.getViewport(0).setBackgroundColour(ogre.ColourValue().Black)
		#self.FOWTarget.getViewport(0).setDimensions(0,0,1,1)

		self.FOWTarget.setAutoUpdated(False)
		self.FOWTarget.update()
		self.FOWTarget.setPriority(1)

		#Hook into FOW and steal its rendering
		shared.FowManager.renderTargets.append(self.FOWTarget)

		print("------------------------------------------------------------\n")

		# #Hook into FOW and steal its rendering
		# self.FOWTarget = self.texture.getBuffer().getRenderTarget() 
		# self.FOWTarget.addViewport(self.camera) 
		# self.FOWTarget.getViewport(0).setOverlaysEnabled(False)
		# self.FOWTarget.getViewport(0).setClearEveryFrame(False)
		# self.FOWTarget.setAutoUpdated(False)
		# self.FOWTarget.getViewport(0).clear()
		# self.FOWTarget.update()  
		# self.FOWTarget.getViewport(0).setBackgroundColour(ogre.ColourValue().Black)
		# self.FOWTarget.setPriority(1) # as we want the plane to be rendered first, set this target's rendering priority to 1 (0 is first)

		# debug.RCC("gui_hideall")
		# self.viewPort = shared.render.root.getAutoCreatedWindow().addViewport(self.camera, 1, 0, 0.8, 0.2, 0.2)
		# self.viewPort.setClearEveryFrame(True)
		# self.viewPort.setAutoUpdated(True)

		# self.camera = shared.render3dScene.sceneManager.createCamera("minimapCam")
		# self.camera.setAspectRatio(self.tsizex/self.tsizey)
		# #self.camera.nearClipDistance = 100
		# #self.camera.setFarClipDistance(1000)
		# self.camera.setProjectionType(ogre.PT_ORTHOGRAPHIC)
		# self.camera.setOrthoWindowWidth(self.tsizex)
		# self.camera.setOrthoWindowHeight(self.tsizey)

		# self.camNode = shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode()
		# self.camNode.attachObject(self.camera)
		# self.camNode.setPosition(self.tsizex/2, 700, self.tsizey/2)
		# self.camera.lookAt((self.tsizex/2)+0.01, 1, (self.tsizey/2))

		debug.RCC("gui_hideall")
		self.viewPort = shared.render.root.getAutoCreatedWindow().addViewport(self.camera, 1, 0, 0.8, 0.2, 0.2)