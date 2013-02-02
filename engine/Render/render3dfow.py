#Render3dExtension - render3dfow
#Classes for rendering the Field Of War effect
#Lowlevel module

from engine import shared, debug
from engine.shared import DPrint
import ogre.renderer.OGRE as ogre
from random import randrange

class FieldOfWar():
	def __init__(self):
		DPrint("Render3dFOW",0,"Initializing Field Of War")

		worldsize=1500
		precision=10
		DPrint("Render3dFOW",0,"World Size: "+str(worldsize))
		DPrint("Render3dFOW",0,"Precision: "+str(precision))

		DPrint("Render3dFOW",0,"Calculating Vertices")
		self.XGrid=[]
		for x in range(0,(worldsize+precision)/precision):
			self.XGrid.append(x*precision)

		self.YGrid=[]
		for y in range(0,(worldsize+precision)/precision):
			self.YGrid.append(y*precision)

		Vertcount=len(self.XGrid)*len(self.YGrid)
		DPrint("Render3dFOW",0,"Vertice Count: "+str(Vertcount))
		Tricount=Vertcount*2
		DPrint("Render3dFOW",0,"Approx. Triangle Count: "+str(Tricount))

		DPrint("Render3dFOW",0,"Creating Plane...")
		self.plane=ogre.ManualObject("Quad")
		self.plane.begin("transparency", ogre.RenderOperation.OT_TRIANGLE_LIST)
		self.plane.setDynamic(True)
		width = worldsize
		height = worldsize


		#May be slow to update with highpres fowplanes! 
		#Todo: Sectionize based on presision
		DPrint("Render3dFOW",0,"Creating Vertices")
		I=0
		self.VertColour=[]
		for x in self.XGrid:
			for y in self.YGrid:
				self.plane.position(x, 0, y)
				#self.plane.colour(randrange(0,10,1)/float(10),randrange(0,10,1)/float(10),randrange(0,10,1)/float(10),0.5) #Uncomment this for pretty colours! <3 <3 :D
				#self.plane.index(I)
				self.plane.colour(0,0,0,0.8)
				self.VertColour.append((0,0,0,0.8))
				I=I+1
		
		What=(worldsize/precision)+1
		self.OppVal=What
		#Create a list of all vertices
		self.VertList=[]
		for x in self.XGrid:
			for y in self.YGrid:
				self.VertList.append((x,y))

		DPrint("Render3dFOW",0,"Calculating triangles")
		#Create a list of all triangles (1)
		self.TriList1=[]
		for x in self.VertList:
			self.TriList1.append((self.VertList.index(x), self.VertList.index(x)+1, self.VertList.index(x)+What))

		#Remove bad triangles (1)
		for x in range(1, What+1):
			self.TriList1.pop((What-1)*x)

		#Remove offchart triangles (1)
		for x in range(1,What):
			self.TriList1.pop(len(self.TriList1)-1)

		#Create a list of all triangles (2)
		self.TriList2=[]
		for x in self.VertList:
			self.TriList2.append((self.VertList.index(x)+What, self.VertList.index(x)+What+1, self.VertList.index(x)+1))

		#Remove bad triangles (2)
		for x in range(1, What+1):
			self.TriList2.pop((What-1)*x)

		#Remove offchart triangles (2)
		for x in range(1,What):
			self.TriList2.pop(len(self.TriList2)-1)

		DPrint("Render3dFOW",0,"Total Triangle count: "+str(len(self.TriList1)+len(self.TriList2)))

		DPrint("Render3dFOW",0,"Creating triangles..")
		for x in self.TriList1:
			self.plane.triangle(x[2],x[1],x[0])

		for x in self.TriList2:
			self.plane.triangle(x[0],x[1],x[2])

		# for I in range(0,worldsize/precision):
		# 	self.plane.index(I,I+1)

		# self.plane.position(0, 0, 0)
		# self.plane.colour(0,0,0,0.5)
		# self.plane.position(width, 0, 0)
		# self.plane.colour(0,0,0,0.5)
		# self.plane.position(0, 0, height)
		# self.plane.colour(0,0,0,0.5)
		# self.plane.position(width, 0, height)
		# self.plane.colour(0,0,0,0.5)
		# self.plane.triangle(3,2,1)
		# self.plane.triangle(0,1,2)
		self.plane.end()

		DPrint("Render3dFOW",0,"Plane created successfully")

		self.plane.setVisible(True)
		self.FOWn=shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode("FieldOfWar")
		self.FOWn.attachObject(self.plane)
		self.FOWn.rotate((1,0,0),ogre.Degree(180))
		self.FOWn.rotate((0,1,0),ogre.Degree(90))
		self.FOWn.setPosition(0,100,0)

	def Update(self):
		#Updates the fogplane
		self.plane.beginUpdate(0)
		for XY in self.VertList:
			self.plane.position(XY[0], 0, XY[1])
			Index=self.VertList.index(XY)
			if self.VertColour[Index][3]==0:
				print(Index)
			self.plane.colour(self.VertColour[Index][0],self.VertColour[Index][1],self.VertColour[Index][2],self.VertColour[Index][3])

		for x in self.TriList1:
			self.plane.triangle(x[2],x[1],x[0])

		for x in self.TriList2:
			self.plane.triangle(x[0],x[1],x[2])
		self.plane.end()
		#self.FOWn.attachObject(self.plane)

	def GetVerts(self):
		return self.VertColour

	def GetVert(self, index):
		return self.VertColour[index]

	#May be slow with big vertlists! Maybe premake a dict where you can lookup the positions for the vertices?
	#Round X,Z to the nearest presisionlevel, and check the dict by using pos as key
	def ConvXZtoVertex(self, pos):
		#Converts a worldcoord into a vertexindex on the fogplane and returns it
		RealPos=(pos[1],pos[0]) #invert the positions
		Prev=100
		PVert=None
		for x in self.VertList:
			foo=abs(x[0]-RealPos[0])+abs(x[1]-RealPos[1])
			if foo<Prev:
				Prev=foo
				PVert=x
		return self.VertList.index(PVert)

	def VisionIdx(self, index):
		#Lights the vertex on the fogplane
		self.VertColour[index]=(0,0,0,0)

	def VisionIdxList(self, ilist):
		for x in ilist:
			self.VertColour[x]=(0,0,0,0)

	def VisionPos(self, pos):
		#Converts a worldcoord into a vertexindex on the fogplane and lights it
		RealPos=(pos[1],pos[0]) #invert the positions
		Prev=100
		PVert=None
		for x in self.VertList:
			foo=abs(x[0]-RealPos[0])+abs(x[1]-RealPos[1])
			if foo<Prev:
				Prev=foo
				print Prev
				PVert=x
		self.VisionIdx(self.VertList.index(PVert))
		return PVert

	def VisionCircle(self, pos, radius):
		#Converts a circle with a radius worldcoords/vertexindexes and lights them
		Outline=[]
		CurrVert=self.ConvXZtoVertex(pos)
		Outline.append(CurrVert)
		for x in range(0,radius):
			CurrVert=CurrVert+1
			Outline.append(CurrVert)
			#print(CurrVert)
			CurrVert=CurrVert+self.OppVal
			Outline.append(CurrVert)
			#print(CurrVert)
		CurrVert=CurrVert+1
		Outline.append(CurrVert)
		#print(CurrVert)
		for x in range(0,radius):
			CurrVert=CurrVert-self.OppVal
			Outline.append(CurrVert)
			#print(CurrVert)
			CurrVert=CurrVert+1
			Outline.append(CurrVert)
			#print(CurrVert)
		CurrVert=CurrVert-self.OppVal
		Outline.append(CurrVert)
		#print(CurrVert)
		for x in range(0, radius):
			CurrVert=CurrVert-1
			Outline.append(CurrVert)
			#print(CurrVert)
			CurrVert=CurrVert-self.OppVal
			Outline.append(CurrVert)
			#print(CurrVert)
		CurrVert=CurrVert-1
		Outline.append(CurrVert)
		#print(CurrVert)
		for x in range(0, radius):
			CurrVert=CurrVert+self.OppVal
			Outline.append(CurrVert)
			#print(CurrVert)
			CurrVert=CurrVert-1
			Outline.append(CurrVert)
			#print(CurrVert)
		CurrVert=CurrVert-self.OppVal
		Outline.append(CurrVert)
		print("______________________________")
		print(Outline)

		self.VisionIdxList(Outline)

	def VisionSquare(self, p0, p2):
		#Converts a square with the specified boundaries into wcords/Vidx and lights it
		distx=abs(p0[0]-p2[0])
		disty=abs(p0[1]-p2[1])
		print (distx, disty)

		p1=(p0[0]+distx, p0[1])
		p3=(p2[0]-distx, p2[1])

		pv0=self.ConvXZtoVertex(p0)
		pv1=self.ConvXZtoVertex(p1)
		pv2=self.ConvXZtoVertex(p2)
		pv3=self.ConvXZtoVertex(p3)

		print(p0, p1, p2, p3)
		print(pv0, pv1, pv2, pv3)

		vdistx=pv1-pv0
		vdisty=pv2-pv3

		print(vdistx, vdisty)

		CurrVert=pv0
		for x in range(0, vdistx):
			for y in range(0, vdisty):
				self.VisionIdx(CurrVert)
				print CurrVert
				CurrVert+=1
			CurrVert=CurrVert+self.OppVal-vdisty


	def VisionBox(self, p0, p1, p2, p3):
		#Converts a box with the specified boundaries worldcoords/vertexindexes and lights them
		pv0=self.ConvXZtoVertex(p0)
		pv1=self.ConvXZtoVertex(p1)
		pv2=self.ConvXZtoVertex(p2)
		pv3=self.ConvXZtoVertex(p3)

		vdistx=abs(pv1-pv0)
		vdisty=abs(pv2-pv3)

		print(vdistx, vdisty)

		CurrVert=pv0
		for x in range(0, vdistx):
			for y in range(0, vdisty):
				self.VisionIdx(CurrVert)
				print CurrVert
				CurrVert+=1
			CurrVert=CurrVert+self.OppVal-vdisty

	def VisionList(self, wlist):
		#Converts a list of worldcoords into indexes and lights them
		for x in wlist:
			self.VisionIdx(self.ConvXZtoVertex(x))


# class FieldOfWar():
# 	def __init__(self):
# 		plane=ogre.Plane((0,1,0),0)
# 		MeshManager=ogre.MeshManager.getSingleton()
# 		MeshManager.createPlane("FOW", "General", plane, 10000, 10000, 100, 100, True, 1, 100, 100, (0,0,1))
# 		self.Entity=shared.render3dScene.sceneManager.createEntity("FOW","FOW")
# 		self.Entity.setMaterialName("FOWDarken")
# 		self.Entity.setCastShadows(False)
# 		#self.Entity.setRenderQueueGroup(ogre.RENDER_QUEUE_SKIES_LATE)
# 		self.node=shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode()
# 		self.node.attachObject(self.Entity)
# 		self.node.setPosition((0,200,0))

# 	def Create(self, pos):
# 		return Vision(pos)

# class Vision():
# 	def __init__(self, pos):
# 		plane=ogre.Plane((0,1,0),0)
# 		MeshManager=ogre.MeshManager.getSingleton()
# 		MeshManager.createPlane("FOWVision", "General", plane, 100, 100, 1, 1, True, 1, 1, 1, (0,0,1))
# 		self.Entity=shared.render3dScene.sceneManager.createEntity("FOW"+str(randrange(0,9999,1)),"FOWVision")
# 		self.Entity.setMaterialName("FOWCircle")
# 		self.Entity.setCastShadows(False)
# 		#self.Entity.setRenderQueueGroup(ogre.RENDER_QUEUE_SKIES_LATE)
# 		self.node=shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode()
# 		self.node.attachObject(self.Entity)
# 		self.node.setPosition(pos)


# 	def setPosition(self, pos):
# 		self.node.setPosition(pos)