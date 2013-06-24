#Render3dExtension - render3dshapes
#Classes for making simple shapes
#Lowlevel module

from engine import shared, debug
from engine.shared import DPrint
import ogre.renderer.OGRE as ogre

def Line(Name, material, Start, End, Mesh=None):
	DPrint("Render3dShapes",0,"Defining Line: "+Name+" with material "+material+" and pos: "+str(SizeX)+" -> "+str(SizeY))
	line=ogre.ManualObject("Line")
	line.begin(material, ogre.RenderOperation.OT_LINE_LIST)
	line.position(Start)
	line.position(End)
	line.end()
	if not Mesh==None:
		line.convertToMesh(Name)
	return line

def Path(Name, material, aPath, Mesh=None):
	DPrint("Render3dShapes",0,"Defining Path: "+Name+" with material "+material+" and path: "+str(aPath))
	line=ogre.ManualObject("Path")
	line.begin(material, ogre.RenderOperation.OT_LINE_LIST)
	prev = None

	for x in aPath:
		# if prev!=None:
		# 	line.position(prev)

		# line.position(x)

		# if aPath.index(x) % 2 == 1:
		# 	prev=x
		# else:
		# 	prev = None

		line.position(x)
		if aPath.index(x)!=len(aPath)-1:
			line.position(aPath[aPath.index(x)+1])

	line.end()
	if not Mesh==None:
		line.convertToMesh(Name)
	return line

def Quad(Name, material, SizeX, SizeZ, Mesh=None):
	DPrint("Render3dShapes",0,"Defining Quad: "+Name+" with material "+material+" and size: "+str((SizeX,SizeY)))
	decal=ogre.ManualObject("Quad")
	decal.begin(material, ogre.RenderOperation.OT_TRIANGLE_LIST)

	width = SizeX
	height = SizeZ
	vec = ogre.Vector3(width / 2, 0, 0)
	for i in range(0, 3):
		decal.position(-vec.x, height, -vec.z)
		decal.textureCoord(0, 0)
		decal.position(vec.x, height, vec.z)
		decal.textureCoord(1, 0)
		decal.position(-vec.x, 0, -vec.z)
		decal.textureCoord(0, 1)
		decal.position(vec.x, 0, vec.z)
		decal.textureCoord(1, 1)

		offset = i * 4
		decal.triangle(offset, offset+3, offset+1)
		decal.triangle(offset, offset+2, offset+3)

	# decal.position(-size, -size, 0.0)
	# decal.textureCoord(0, 0)
	# decal.position(size,-size,0.0)
	# decal.position(size, size,0.0)
	# decal.position(-size,size,0.0)
	# decal.position(-size,-size,0.0)
	decal.end()
	if not Mesh==None:
		decal.convertToMesh(Name)
	return decal

def Tetra(Name, material, scale, Mesh=None):
	DPrint("Render3dShapes",0,"Defining Tetrahedron: "+Name+" with material "+material+" and scale: "+str(scale))
	shape=ogre.ManualObject("Tetra")

	Vec=[0,0,0,0]
	mbot=scale*0.2
	mtop=scale*0.62
	mf=scale*0.289
	mb=scale*0.577
	mlr=scale*0.5
	Vec[0]=(-mlr,-mbot,mf)
	Vec[1]=(mlr,-mbot,mf)
	Vec[2]=(0,-mbot,-mb)
	Vec[3]=(0,mtop,0)

	#Bottom
	shape.begin(material, ogre.RenderOperation.OT_TRIANGLE_LIST)
	shape.position(Vec[2])
	shape.textureCoord(0, 0)
	shape.position(Vec[1])
	shape.textureCoord(1, 0)
	shape.position(Vec[0])
	shape.textureCoord(0, 1)
	shape.triangle(0,1,2)
	shape.textureCoord(1, 1)
	shape.end()

	#Right Backside
	shape.begin(material, ogre.RenderOperation.OT_TRIANGLE_LIST)
	shape.position(Vec[1])
	shape.position(Vec[2])
	shape.position(Vec[3])
	shape.triangle(0,1,2)
	shape.textureCoord(1, 0)
	shape.end()

	#Left backside
	shape.begin(material, ogre.RenderOperation.OT_TRIANGLE_LIST)
	shape.position(Vec[3])
	shape.position(Vec[2])
	shape.position(Vec[0])
	shape.triangle(0,1,2)
	shape.textureCoord(0, 1)
	shape.end()

	#Front
	shape.begin(material, ogre.RenderOperation.OT_TRIANGLE_LIST)
	shape.position(Vec[0])
	shape.position(Vec[1])
	shape.position(Vec[3])
	shape.triangle(0,1,2)
	shape.textureCoord(1, 1)
	shape.end()
	
	if not Mesh==None:
		shape.convertToMesh(Name)
	return shape

def WTetra():
	pass

def CustomTetra():
	pass

def Cube():
	pass

def CustomCube():
	pass

def Circle():
	pass

def Sylinder():
	pass

def Sphere():
	pass