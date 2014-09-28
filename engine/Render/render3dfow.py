#http://www.youtube.com/watch?feature=player_embedded&v=VjGSMUep6_4

import ogre.renderer.OGRE as ogre
import math
from engine import shared, debug
from engine.World import posalgo
from traceback import print_exc

class FogOfWarListener(ogre.RenderTargetListener,ogre.Node.Listener):
	def __init__(self):
		ogre.RenderTargetListener.__init__(self)
		ogre.Node.Listener.__init__(self)
		#self.terrain = terrain # this is a string corresponding to the name of the terrain material. Ex: "OceanCg" DEPREACIATED

		self.created=False
		self.whiteOutToggle=False

		debug.ACC("fow_add", self.ChangeShit, info="Add a FOW view", args=2)
		debug.ACC("dbg_fow", self.debugView, info="Show FowCam viewPort", args=0)
		debug.ACC("fow_white", self.whiteOut, info="'Disable' Fog of War", args=0)
		debug.ACC("fow_srot", self.debugRot, info="Rotate FOW Camera", args=3)
		debug.ACC("fow_spos", self.debugPos, info="Set FOW Camera Position", args=3)
		debug.ACC("fow_stra", self.debugTra, info="Set FOW Camera translation", args=3)

		self.AllyNodes={}
		self.EnemyNodes={}

		self.CircleEnts=[]
		self.CircleNodes=[]
		
	def whiteOut(self):
		if not self.whiteOutToggle:
			self.fogManager.setAmbientLight(ogre.ColourValue(1,1,1))
			#self.planeMesh.getSubMesh(0).setMaterialName("FOW_circleMat")
			self.whiteOutToggle=True
			self.terrainTarget.update()
		else:
			self.fogManager.setAmbientLight(ogre.ColourValue(0.2,0.2,0.2))
			self.whiteOutToggle=False
			self.terrainTarget.update()

	def Create(self, tsizex, tsizey, terrainMat):
		shared.DPrint("FOWManager", 1, "Creating Fog Of War")

		self.created=True

		self.tsizex=tsizex #Terrain Size
		self.tsizey=tsizey
		self.tsize=((tsizex+tsizey)/2) 
		self.camalt = self.tsize + 1000 #Find out an algorithm to calculate this properly (HARDCODE)

		self.fogManager = ogre.Root.getSingleton().createSceneManager(ogre.ST_EXTERIOR_CLOSE)
		self.fogManager.setAmbientLight(ogre.ColourValue(0.2,0.2,0.2))

		self.camera = self.fogManager.createCamera("fogCam")
		self.camera.setAspectRatio(self.tsizex/self.tsizey)
		self.camera.nearClipDistance = 10
		self.camera.setFarClipDistance(10000)

		self.camnode = self.fogManager.getRootSceneNode().createChildSceneNode()
		self.camnode.attachObject(self.camera)

		self.camera.setProjectionType(ogre.PT_ORTHOGRAPHIC)
		self.camera.setOrthoWindowHeight(self.tsizey)
		self.camera.setOrthoWindowWidth(self.tsizex)
		#self.camera.setFOVy(ogre.Radian(50))
		self.camnode.setPosition(self.tsizex/2, self.tsize, self.tsizey/2) 
		self.camera.lookAt((self.tsizex/2)+0.01, 1, (self.tsizey/2))
		

		#"FOG" (Black plane)
		#__________________________________________________________________________________________________________________________________________________________

		#create the plane
		self.plane = ogre.MovablePlane("ReflectPlane")
		self.plane.d = 0
		self.plane.normal = ogre.Vector3().UNIT_Y

		#ogre.MeshManager.getSingleton().createPlane(name,              group,                                                plane, width, height, xseg, yseg, Normals, texcoodsets, utile, vtile, upvector)
		self.planeMesh = ogre.MeshManager.getSingleton().createPlane("ReflectionPlane", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME,self.plane, self.tsizex, self.tsizey, 1, 1, True, 1, 1, 1, ogre.Vector3().UNIT_Z)
		self.planeEnt = self.fogManager.createEntity( "Plane", "ReflectionPlane" ) 
		self.planeNode = self.fogManager.getRootSceneNode().createChildSceneNode() 
		self.planeNode.attachObject(self.planeEnt) 
		self.planeNode.setPosition(self.tsizex/2,0,self.tsizey/2) #Set plane directly over the terrain

		#__________________________________________________________________________________________________________________________________________________________

		#establish the entity that will act as each ally's vision sight range
		circle = ogre.MovablePlane("circleMovablePlane") 
		circle.normal = ogre.Vector3().UNIT_Y 
		circle.d = 0 

		# construct a white circle material that can be blended on the Overlay plane to create the sight radius light area
		circleMat = ogre.MaterialManager.getSingleton().create("FOW_circleMat",ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME) 
		circleMat.getTechnique(0).getPass(0).createTextureUnitState("FOWbeta7.png")
		circleMat.setSelfIllumination(1,1,1) #make sure the image is always perfectly lit
		circleMat.setSceneBlending(ogre.SBT_TRANSPARENT_ALPHA)
		circleMat.setDepthWriteEnabled(False)

		# attach the material to a mesh that we can attach to ally nodes
		mesh = ogre.MeshManager.getSingleton().createPlane("FOW_Circle", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME, circle, 500, 500, 1, 1, True, 1, 1, 1, ogre.Vector3().UNIT_Z)
		mesh.getSubMesh(0).setMaterialName("FOW_circleMat")

		#__________________________________________________________________________________________________________________________________________________________

		self.texture = ogre.TextureManager.getSingleton().createManual( "RttTex", "General", ogre.TextureType.TEX_TYPE_2D, 2048, 2048, 1, ogre.PixelFormat.PF_R8G8B8, ogre.TU_RENDERTARGET )
		#self.texture = ogre.TextureManager.getSingleton().createManual( "name", "group", texturetype, width, height, depth, pixelformat, ogre.TU_RENDERTARGET) 
		self.RT = self.texture.getBuffer().getRenderTarget()

		#terrainMat = terrainmat
		self.terrainPass = terrainMat.getTechnique(0).createPass()
		self.terrainPass.setSceneBlending(ogre.SBT_MODULATE) # mutliply the color value contents of the scene with the values in this texture pass
	
		# modify the properties of this texture and make it a state within the pass created earlier
		tex = self.terrainPass.createTextureUnitState("RttTex") 
		tex.setProjectiveTexturing(True,self.camera) # allow the texture to be updated via projections from self.camera
		tex.setTextureAddressingMode(ogre.TextureUnitState.TAM_CLAMP) # when color values go above 1.0, they are set to 1.0 

		#associate render target with the texture that was just made
		self.terrainTarget = self.texture.getBuffer().getRenderTarget() 
		self.terrainTarget.addViewport(self.camera) 
		self.terrainTarget.getViewport(0).setOverlaysEnabled(False)
		self.terrainTarget.getViewport(0).setClearEveryFrame(False)
		self.terrainTarget.setAutoUpdated(False)
		self.terrainTarget.getViewport(0).clear()
		self.terrainTarget.update()  
		self.terrainTarget.getViewport(0).setBackgroundColour(ogre.ColourValue().Black)
		self.terrainTarget.setPriority(1) # as we want the plane to be rendered first, set this target's rendering priority to 1 (0 is first)

	def update(self):
		self.terrainTarget.update()

	def addView(self, size):
		size = float(size)/float(256)
		circleEnt = self.fogManager.createEntity( "Circle"+str(len(self.CircleEnts)), "FOW_Circle" ) 
		circleEnt.setCastShadows(False)
		circleNode = self.fogManager.getRootSceneNode().createChildSceneNode() 
		circleNode.attachObject(circleEnt)
		circleNode.setPosition(0, 1+(len(self.CircleEnts)/10), 0)
		circleNode.setScale(1*size, 1*size, 1*size)
		circleNode.showBoundingBox(False)

		self.CircleEnts.append(circleEnt)
		self.CircleNodes.append(circleNode)

		return (circleEnt, circleNode, size)

	def rmView(self, Index):
		Index["node"].detachObject(Index["ent"])
		shared.render3dScene.sceneManager.destroyEntity(Index["ent"].getName())
		#shared.render3dScene.sceneManager.destroySceneNode(Index["node"].getName())
		self.update()

	def changeNodeSize(self, node, size):
		size = float(size)/float(256)
		node.setScale(1*size, 1*size, 1*size)

	def nodeUpdate(self, node):
		if node.getName() in self.EnemyNodes:
			EnodeIndex = self.EnemyNodes[node.getName()]
			Enode = EnodeIndex["node"]
			EnodePos = self.ogre2pyNodeCoord(Enode)

			#print("Enode Defaulting to False")
			EnodeIndex["viewedby"]=[]

			for AnodeName, AnodeIndex in self.AllyNodes.iteritems():
				Anode = AnodeIndex["node"]
				AnodePos = self.ogre2pyNodeCoord(Anode)

				if posalgo.in_circle(AnodePos[0], AnodePos[2], AnodeIndex["size"]-5, EnodePos[0], EnodePos[2]):
					#print("ENODE: Unit is in circle! VISIBLE")
					#print(AnodePos[0], AnodePos[2], 256, EnodePos[0], EnodePos[2])
					AnodeIndex["vision"].append(EnodeIndex)
					EnodeIndex["viewedby"].append(AnodeIndex)
					Enode.setVisible(True)
				else:
					if EnodeIndex in AnodeIndex["vision"]:
						#print("ENODE: Im not visible for him, removing myself")
						AnodeIndex["vision"].remove(EnodeIndex)

			if len(EnodeIndex["viewedby"])==0:
				Enode.setVisible(False)



		elif node.getName() in self.AllyNodes:
			AnodeIndex=self.AllyNodes[node.getName()]
			Anode = AnodeIndex["node"]

			AnodePos = self.ogre2pyNodeCoord(Anode)

			#Set new view placement
			#print("___________________________________________________________________________________________________________________________________________________________")
			#print("NodeName: %s" % (node.getName()))
			node._updateBounds()
			Anode._updateBounds()
			UnitPos=node._getWorldAABB().getCenter()
			#UnitPos=node.getPosition()
			#print(UnitPos)
			AnodePos=Anode.getPosition()
			#print(AnodePos)
			AnodeCenter=Anode._getWorldAABB().getCenter()
			#print(AnodeCenter)
			AnodeSize=Anode._getWorldAABB().getHalfSize()
			#print(AnodeSize)
			#Offset = (AnodePos.x-AnodeCenter.x, AnodePos.z-AnodeCenter.z)
			#Offset = (AnodeSize.x, AnodeSize.z)
			Offset = (0,0)
			#print(Offset)
			#Anode.setPosition(UnitPos.x-(Offset.x/2), AnodePos[1], UnitPos.z-(Offset.z/2))
			Anode.setPosition(UnitPos.x-Offset[0], AnodePos[1], UnitPos.z-Offset[1])
			#print(UnitPos.x-Offset[0], AnodePos[1], UnitPos.z-Offset[1])

			#Update the fowplane with the new viewplacements
			self.update()

			#Set everything that was previously in view, to be invision if they are not in viewrange anymore
			for EnodeIndex in AnodeIndex["vision"]:
				if AnodeIndex in EnodeIndex["viewedby"]:
					#print("ANODE: Removing myself from Enode")
					EnodeIndex["viewedby"].remove(AnodeIndex)

					if len(EnodeIndex["viewedby"])==0:
						#print("ANODE: Enode is empty, hiding")
						EnodeIndex["node"].setVisible(False)
				#print(EnodeIndex)

			AnodeIndex["vision"] = []

			#Find everything that is currently in the units view now
			for EnodeName, EnodeIndex in self.EnemyNodes.iteritems():
				Enode = EnodeIndex["node"]
				EnodePos = self.ogre2pyNodeCoord(Enode)

				if posalgo.in_circle(AnodePos[0], AnodePos[2], AnodeIndex["size"]-5, EnodePos[0], EnodePos[2]):
					#print("ANODE: Unit is in circle! VISIBLE")
					AnodeIndex["vision"].append(EnodeIndex)
					EnodeIndex["viewedby"].append(AnodeIndex)
					Enode.setVisible(True)

		else:
			print("Node not found!")
			print node

	def addAlly(self, node, viewsize):
		tupview = self.addView(viewsize)
		allynodeIndex = {"ent":tupview[0], "node":tupview[1], "size":viewsize, "vision":[]}

		self.AllyNodes[node.getName()]=allynodeIndex
		self.nodeUpdate(node)

		return allynodeIndex

	def addEnemy(self, node):
		enemynodeIndex = {"node":node, "viewedby":[]}

		self.EnemyNodes[node.getName()]=enemynodeIndex
		self.nodeUpdate(node)

		return enemynodeIndex

	def rmNode(self, node):
		if node.getName() in self.AllyNodes:
			self.rmView(self.AllyNodes[node.getName()])
			del self.AllyNodes[node.getName()]
		elif node.getName() in self.EnemyNodes:
			del self.EnemyNodes[node.getName()]

	def chViewSize(self, node, viewsize):
		nodename = node.getName()
		print("Changing View Size")
		if nodename in self.AllyNodes:
			NodeIndex = self.AllyNodes[nodename]
			NodeIndex["size"] = viewsize
			self.changeNodeSize(NodeIndex["node"])
		else:
			print("Node not in our ally Index!")

	def ChangeShit(self, x, z):
		#self.circleNode.setPosition(float(x),float(y),float(z))
		self.addView(200)[1].setPosition(float(x), 1, float(z))
		self.update()

	def debugView(self):
		self.viewPort = shared.render.root.getAutoCreatedWindow().addViewport(self.camera, 1, 0 ,0.8 ,0.2 ,0.2)
		debug.RCC("gui_hideall")
		return "Run gui_showall to get the GUI back on"

	def ogre2pyNodeCoord(self, node):
		if type(node) == str:
			print(node)
		else:
			return (int(node.getPosition().x), int(node.getPosition().y), int(node.getPosition().z))

	def debugRot(self, x, y, z):
		x, y, z = float(x), float(y), float(z)
		self.camnode.lookAt(x, y, z)

	def debugPos(self, x, y, z):
		x, y, z = float(x), float(y), float(z)
		self.camnode.setPosition(x, y, z) 
		
	def debugTra(self, x, y, z):
		x, y, z = float(x), float(y), float(z)
		#x, y, z = x, y, z + tuple(self.camera.getPosition())
		
		self.camnode.translate(x, y, z) 