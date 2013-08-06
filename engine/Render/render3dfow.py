#http://www.youtube.com/watch?feature=player_embedded&v=VjGSMUep6_4

import ogre.renderer.OGRE as ogre
import math
from engine import shared, debug
from engine.World import posalgo
from traceback import print_exc

class FogOfWarListener(ogre.RenderTargetListener,ogre.Node.Listener):
	def __init__(self, terrain):
		ogre.RenderTargetListener.__init__(self)
		ogre.Node.Listener.__init__(self)
		self.terrain = terrain # this is a string corresponding to the name of the terrain material. Ex: "OceanCg"

		self.created=False

		debug.ACC("turn", self.ChangeShit, info="Enable a nein", args=3)

		self.AllyNodes={}
		self.EnemyNodes={}

		self.CircleEnts=[]
		self.CircleNodes=[]

		
	def Create(self, tsizex, tsizey):
		shared.DPrint("FOWManager", 1, "Creating Fog Of War")

		self.created=True

		self.tsizex=tsizex #Terrain Size
		self.tsizey=tsizey
		self.tsize=(tsizex+tsizey)/2

		self.fogManager = ogre.Root.getSingleton().createSceneManager(ogre.ST_EXTERIOR_CLOSE)
		self.fogManager.setAmbientLight(ogre.ColourValue(0.2,0.2,0.2))

		self.camera = self.fogManager.createCamera("fogCam")
		self.camera.setAspectRatio(1)
		#self.camera.setProjectionType(ogre.PT_ORTHOGRAPHIC)
		self.camera.setPosition(self.tsizex, self.tsize, self.tsizey) 
		self.camera.lookAt(self.tsizex/2, 0, (self.tsizey/2)+1)
		self.camera.nearClipDistance = 10
		self.camera.setFarClipDistance(10000)

		#"FOG" (Black plane)
		#__________________________________________________________________________________________________________________________________________________________

		#create the plane
		self.plane = ogre.MovablePlane("ReflectPlane")
		self.plane.d = 0
		self.plane.normal = ogre.Vector3().UNIT_Y

		#ogre.MeshManager.getSingleton().createPlane(name,              group,                                                plane, width, height, xseg, yseg, Normals, texcoodsets, utile, vtile, upvector)
		ogre.MeshManager.getSingleton().createPlane("ReflectionPlane", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME,self.plane, self.tsizex, self.tsizey, 1, 1, True, 1, 1, 1, ogre.Vector3().UNIT_Z)
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
		circleMat.getTechnique(0).getPass(0).createTextureUnitState("FOWbeta4.png")
		circleMat.setSelfIllumination(1,1,1) #make sure the image is always perfectly lit
		circleMat.setSceneBlending(ogre.SBT_TRANSPARENT_ALPHA)
		circleMat.setDepthWriteEnabled(False)

		# attach the material to a mesh that we can attach to ally nodes
		mesh = ogre.MeshManager.getSingleton().createPlane("FOW_Circle", ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME, circle, 500, 500, 1, 1, True, 1, 1, 1, ogre.Vector3().UNIT_Z)
		mesh.getSubMesh(0).setMaterialName("FOW_circleMat")

		#__________________________________________________________________________________________________________________________________________________________

		self.texture = ogre.TextureManager.getSingleton().createManual( "RttTex", "General", ogre.TextureType.TEX_TYPE_2D, 512, 512, 1, ogre.PixelFormat.PF_R8G8B8, ogre.TU_RENDERTARGET )
		#self.texture = ogre.TextureManager.getSingleton().createManual( "terrainTex", "General", ogre.TEX_TYPE_2D, 512, 512, 0, ogre.PF_R8G8B8, ogre.TU_RENDERTARGET) 
		self.RT = self.texture.getBuffer().getRenderTarget()

		terrainMat = ogre.MaterialManager.getSingleton().getByName(self.terrain)
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
		circleNode = self.fogManager.getRootSceneNode().createChildSceneNode() 
		circleNode.attachObject(circleEnt) 
		circleNode.setPosition(0, 1+(len(self.CircleEnts)), 0)
		circleNode.setScale(1*size, 1*size, 1*size)

		self.CircleEnts.append(circleEnt)
		self.CircleNodes.append(circleNode)

		return (circleEnt, circleNode, size)

	def rmView(self, Index):
		Index["node"].detachObject(Index["ent"])
		shared.render3dScene.sceneManager.destroyEntity(Index["ent"].getName())
		#shared.render3dScene.sceneManager.destroySceneNode(Index["node"].getName())
		self.update()

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
			UnitPos=node.getPosition()
			Anode.setPosition(UnitPos.x, AnodePos[1], UnitPos.z)

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

	def ChangeShit(self, x, y, z):
		#self.circleNode.setPosition(float(x),float(y),float(z))
		self.addView(200)[1].setPosition(float(x), 0, float(z))
		self.update()

	def ogre2pyNodeCoord(self, node):
		if type(node) == str:
			print(node)
		else:
			return (int(node.getPosition().x), int(node.getPosition().y), int(node.getPosition().z))