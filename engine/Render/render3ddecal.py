#Render3dExtension - render3ddecal
#Classes for handeling Decals

from engine import shared, debug
from engine.shared import DPrint
from random import randrange
import ogre.renderer.OGRE as ogre

class DecalManager():
	#If you want to make progress here, you got to goddamn figure it out yourself.. this is my try
	def __init__(self):
		self.dcount=0
		self.decals={}

	def Declare(self):
		self.Define("BCircle", "Circle", 1000, 1000)
		self.Define("MCircle", "Circle", 700, 700)
		self.Define("SCircle", "Circle", 400, 400)
		self.Define("SSCircle","Circle", 50, 50)
		self.Define("Move","Move",50,50)
		self.Define("Burnt","Burnt", 50, 50)

	def Define(self, meshname, material, sizex, sizez):
		DPrint(9,0,"Defining Decal: "+meshname+" with material "+material+" as an A2Decal")
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
		DPrint(9,0,"Creating Decal"+meshname+" with id "+str(self.dcount)+" at "+str(pos)+" Rot: "+str(rot))
		self.dcount=self.dcount+1
		return A2Decal(self.dcount,"Decal"+meshname, pos, rot)
		

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
		DPrint(9,0,"Decal "+str(self.ID)+" gc'd")
		#shared.render3dScene.sceneManager.destroyEntity(self.ent)
		#shared.render3dScene.sceneManager.destroySceneNode(self.node)

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
	def __init__(self,mPos, mSize, mTexture, mVisible):
		self.mPos=mPos
		self.mSize=mSize
		self.mTexture=mTexture
		self.mVisible=mVisible
		self.mSceneManager=shared.render3dScene.sceneManager

		self.mDecalFrustum=ogre.Frustum()
		self.mProjectorNode=self.mSceneManager.getRootSceneNode().createChildSceneNode("Decal"+str(randrange(0,900)))
		self.mProjectorNode.attachObject(self.mDecalFrustum)
		self.mProjectorNode.setPosition(mPos)

		self.filterFrustum=ogre.Frustum()
		self.filterFrustum.setProjectionType(ogre.PT_ORTHOGRAPHIC)
		self.filterNode=self.mProjectorNode.createChildSceneNode("DecalFilterNode"+str(randrange(0,900)))
		self.filterNode.attachObject(self.filterFrustum)
		self.filterNode.setOrientation(ogre.Quaternion(ogre.Degree(90),ogre.Vector3().UNIT_Y))

	def makeMaterialReceiveDecal(self, matName):
		mat=ogre.MaterialManager.getSingleton().getByName(matName)
		mPass=mat.getTechnique(0).createPass()

		mPass.setSceneBlending(ogre.SBT_TRANSPARENT_ALPHA)
		mPass.setDepthBias(1)
		mPass.setLightingEnabled(False)
		texState=mPass.createTextureUnitState("decal.png")
		texState.setProjectiveTexturing(True, self.mDecalFrustum)
		texState.setTextureAddressingMode(ogre.TextureUnitState.TAM_CLAMP)
		texState.setTextureFiltering(ogre.FO_POINT, ogre.FO_LINEAR, ogre.FO_NONE)

		texState = mPass.createTextureUnitState("decal_filter.png")
		texState.setProjectiveTexturing(True, self.filterFrustum)
		texState.setTextureAddressingMode(ogre.TextureUnitState.TAM_CLAMP)
		texState.setTextureFiltering(ogre.TFO_NONE)