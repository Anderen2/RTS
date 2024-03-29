#Render3dExtension - render3ddecal
#Classes for handeling Decals

from engine import shared, debug
from engine.shared import DPrint
from random import randrange
from traceback import print_exc
import ogre.renderer.OGRE as ogre
from twisted.internet import reactor

class DecalManager():
	#If you want to make progress here, you got to goddamn figure it out yourself.. this is my try
	def __init__(self):
		self.dcount=0
		self.decals={}

		self.pdecals=[]

		debug.ACC("rdtest", self.TestDecal, info="Decal Test \nargs: x y z", args=3)

	def Declare(self):
		self.Define("BCircle", "Circle", 1000, 1000)
		self.Define("MCircle", "Circle", 700, 700)
		self.Define("SCircle", "Circle", 400, 400)
		self.Define("SSCircle","Circle", 50, 50)
		self.Define("Move","Move",50,50)
		self.Define("Burnt","Burnt", 50, 50)

	def Define(self, meshname, material, sizex, sizez):
		DPrint("Render3dDecal",0,"Defining Decal: "+meshname+" with material "+material+" as an A2Decal")
		self.decal=ogre.ManualObject("A2Decal")
		self.decal.begin(material, ogre.RenderOperation.OT_TRIANGLE_LIST)

		width = sizex
		height = sizez
		vec = ogre.Vector3(width / 2, 0, 0)
		for i in range(0, 3):
			self.decal.position(-vec.x, height, -vec.z)
			self.decal.textureCoord(0, 0)
			self.decal.position(vec.x, height, vec.z)
			self.decal.textureCoord(1, 0)
			self.decal.position(-vec.x, 0, -vec.z)
			self.decal.textureCoord(0, 1)
			self.decal.position(vec.x, 0, vec.z)
			self.decal.textureCoord(1, 1)

			offset = i * 4
			self.decal.triangle(offset, offset+3, offset+1)
			self.decal.triangle(offset, offset+2, offset+3)

		# self.decal.position(-size, -size, 0.0)
		# self.decal.textureCoord(0, 0)
		# self.decal.position(size,-size,0.0)
		# self.decal.position(size, size,0.0)
		# self.decal.position(-size,size,0.0)
		# self.decal.position(-size,-size,0.0)
		self.decal.end()
		self.decal.convertToMesh("Decal"+meshname)

	def Create(self, meshname, pos, rot):
		DPrint("Render3dDecal",0,"Creating Decal"+meshname+" with id "+str(self.dcount)+" at "+str(pos)+" Rot: "+str(rot))
		self.dcount=self.dcount+1
		return A2Decal(self.dcount,"Decal"+meshname, pos, rot)

	def TestDecal(self, posx, posz, size, time):
		try:
			decal=TerrainPDecal((float(posx), float(posz)), float(size), "burnt.png", int(time), True)
			self.pdecals.append(decal)
			#decal.makeMaterialReceiveDecal()
		except:
			print_exc()

class A2Decal():
	def __init__(self, ID, mesh, pos, rot):
		self.ID=ID
		self.name=mesh+str(ID)
		self.ent=shared.render3dScene.sceneManager.createEntity(mesh+str(ID), mesh)
		self.node=shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode("DecalNode"+str(ID))
		self.node.attachObject(self.ent)
		self.node.setPosition(pos)
		self.node.rotate((1,0,0),ogre.Degree(rot[0]))
		self.node.rotate((0,1,0),ogre.Degree(rot[1]))
		self.node.rotate((0,0,1),ogre.Degree(rot[2]))
		#self.node.showBoundingBox(True)

	def SetPosition(self, pos):
		self.node.setPosition(pos)

	def SetRotation(self, rot):
		self.node.rotate((1,0,0),ogre.Degree(rot[0]))
		self.node.rotate((0,1,0),ogre.Degree(rot[1]))
		self.node.rotate((0,0,1),ogre.Degree(rot[2]))

	def __del__(self):
		try:
			#shared.DPrint("Render3dDecal",0,"Decal "+str(self.ID)+" gc'd")
			self.node.detachObject(self.ent)
			shared.render3dScene.sceneManager.destroyEntity(self.ent)
			shared.render3dScene.sceneManager.destroySceneNode(self.node)
		except:
			pass
			#print("Decal "+str(self.ID)+" gc'd")
#__________________________________________________________________________________________________________________________________________________________________________
#Nonworking Decals Ahoy:

class TerrainMDecal():
	def __init__(self):
		print("Creating Decal")
		self.decal=ogre.ManualObject("MeshDecal")
		shared.render3dScene.sceneManager.getRootSceneNode().attachObject(self.decal)
		x_size=4
		z_size=4
		self.decal.begin("blah", ogre.RenderOperation.OT_TRIANGLE_LIST)
		self.decal.setUseIdentityProjection(True)
		self.decal.setUseIdentityView(True)
		self.decal.setQueryFlags(0)
		for x in range(0,x_size):
			for z in range(0, z_size):
				self.decal.position((x, 0, z))
				self.decal.textureCoord(x/x_size, z/z_size)

		for x in range(0,x_size):
			for z in range(0, z_size):
				self.decal.quad(x*(x_size+1)+z, x*(x_size+1)+z+1, (x+1)*(x_size+1)+z+1,(x+1)*(x_size+1)+z)

		self.decal.end()
		self.decal.setVisible(True)

	def SetPos(self, Tx, Tz, z, rad):
		print("Setting position")
		x1=Tx-rad
		z1=Tz-rad
		x_size=4
		z_size=4
		x_step=rad*2/x_size
		z_step=rad*2/z_size
		self.decal.beginUpdate(0)

		for x in range(0,x_size):
			for z in range(0, z_size):
				self.decal.position((x1, z+1, z1))
				self.decal.textureCoord(x/x_size, z/z_size)
				z1+=z_step
			x1+=x_step
			z1=z-rad

		for x in range(0,x_size):
			for z in range(0, z_size):
				self.decal.quad(x*(x_size+1)+z, x*(x_size+1)+z+1, (x+1)*(x_size+1)+z+1,(x+1)*(x_size+1)+z)
		self.decal.end()
		self.decal.convertToMesh("Decal")
		decalMesh=shared.render3dScene.sceneManager.createEntity("Decal",self.decal)

class TerrainPDecal():
	def __init__(self,mPos, mSize, mTexture, time, mVisible):
		self.mPos=mPos
		self.mSize=mSize
		self.mTexture=mTexture
		self.mVisible=mVisible
		self.mSceneManager=shared.render3dScene.sceneManager

		if time!=0:
			reactor.callLater(time, self.Remove)

		self.mDecalFrustum=ogre.Frustum()
		#self.mDecalFrustum.setProjectionType(ogre.PT_ORTHOGRAPHIC)
		#self.mDecalFrustum.setOrthoWindowHeight(100)
		self.mProjectorNode=self.mSceneManager.getRootSceneNode().createChildSceneNode("PDecal"+str(randrange(0,900)))
		self.mProjectorNode.attachObject(self.mDecalFrustum)
		self.mProjectorNode.setPosition(mPos[0], mSize, mPos[1])
		self.mProjectorNode.lookAt((int(mPos[0]), 0, int(mPos[1])), self.mProjectorNode.TS_WORLD)

		if mVisible:
			self.makeMaterialReceiveDecal()

	def makeMaterialReceiveDecal(self):
		mat=shared.render3dTerrain.Material
		mPass=mat.getTechnique(0).createPass()

		mPass.setSceneBlending(ogre.SBT_TRANSPARENT_ALPHA)
		mPass.setLightingEnabled(False)
		texState=mPass.createTextureUnitState(self.mTexture)
		texState.setTextureScale(1, 1)
		texState.setProjectiveTexturing(True, self.mDecalFrustum)
		texState.setTextureAddressingMode(ogre.TextureUnitState.TAM_BORDER)
		texState.setTextureBorderColour(ogre.ColourValue(0.0, 0.0, 0.0, 0.0))
		#texState.setTextureFiltering(ogre.FO_POINT, ogre.FO_LINEAR, ogre.FO_NONE)

	def Remove(self):
		self.mProjectorNode.detachObject(self.mDecalFrustum)
		#shared.render3dScene.sceneManager.destroyEntity(self.ent)
		shared.render3dScene.sceneManager.destroySceneNode(self.mProjectorNode)