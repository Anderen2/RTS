#Rendermodule - render3d
#Classes for rendering 3d enviroment

import render3dent, render3ddecal, render3dwaypoint, render3dwater, render3dcamera
from engine import shared, debug
import ogre.renderer.OGRE as ogre
from ogre.gui.CEGUI import MouseCursor
from random import randrange
from string import split
from math import floor

class Scene():
	def __init__(self):
		self.root=shared.renderRoot

	def Setup(self):
		shared.DPrint("Render3d",1,"Setting up terrain..")
		self.sceneManager = self.root.createSceneManager(ogre.ST_EXTERIOR_CLOSE, "Default sceneManager")
		self.sceneManager.setWorldGeometry ("terrain.cfg")
		shared.DPrint("Render3d",1,"Skybox..")
		self.sceneManager.setSkyBox (True, "Examples/SpaceSkyBox")

		self.EntNode=self.sceneManager.getRootSceneNode().createChildSceneNode("EntNode",(0,0,0))
		self.StatNode=self.sceneManager.getRootSceneNode().createChildSceneNode("StatNode",(0,0,0))

		shared.DPrint("Render3d",1,"Camera..")
		shared.render3dCamera=render3dcamera.Camera(self.root, self)
		self.camera=shared.render3dCamera

		shared.DPrint("Render3d",1,"Particle Parameters")
		ogre.ParticleSystem.defaultNonVisibleUpdateTimeout=1

		shared.DPrint("Render3d",1,"SelectStuff..")
		shared.render3dSelectStuff=SelectStuff(self.root, self)

		shared.DPrint("Render3d",1,"EntityHandeler..")
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
		debug.ACC("r_polymode", self.PolygenMode, info="Change the polygenmode. 1 for points, 2 for wireframe, 3 for solid", args=1)

	def PostFilterEnable(self,PF):
		ogre.CompositorManager.getSingleton().addCompositor(shared.render3dCamera.viewPort, PF)
		ogre.CompositorManager.getSingleton().setCompositorEnabled(shared.render3dCamera.viewPort, PF, True)

	def PostFilterDisable(self,PF):
		ogre.CompositorManager.getSingleton().setCompositorEnabled(shared.render3dCamera.viewPort, PF, False)

	def PolygenMode(self, PM):
		shared.render3dCamera.camera.setPolygonMode(shared.render3dCamera.camera, int(PM))

class SelectStuff():
	def __init__(self, root, scene):
		self.TestStuff=False
		self.scene=scene
		self.root=root
		self.camera=self.scene.camera

		#Plane Selection
		self.LMBSel=False
		self.mStart = ogre.Vector2()
		self.mStop = ogre.Vector2()
		self.mRect = None
		self.mSelecting = False
		shared.DPrint("SelectStuff",1,"SelectStuff: Defining Rectangles..")
		self.mRect = SelectionRectangle("Selection SelectionRectangle")
		scene.sceneManager.getRootSceneNode().createChildSceneNode().attachObject(self.mRect) #Adding a rectangle to the scene
		self.mVolQuery = scene.sceneManager.createPlaneBoundedVolumeQuery(ogre.PlaneBoundedVolumeList()) #Doing shit to the rectangle in the scene
		self.querylistener = PlaneQueryListener(self)

		#Raytrace
		shared.DPrint(2,1,"SelectStuff: Setting up RayTrace")
		self.raySceneQuery = self.scene.sceneManager.createRayQuery(ogre.Ray())

		self.hackhz, self.hackvz = shared.render3dCamera.getDimensions()
		self.CurrentSelection=[]

	def startSelection(self, mousePos):
		self.mStart.x = mousePos.d_x / float(self.hackhz)
		self.mStart.y = mousePos.d_y / float(self.hackvz)
		self.mStop = ogre.Vector2(self.mStart.x+0.00001, self.mStart.y+0.00001)
		self.mSelecting = True
		self.mRect.clear()
		self.mRect.setVisible(True)
		self.mRect.setCorners(self.mStart, self.mStop)

	def moveSelection(self, mousePos):
		self.mStart.x = mousePos.d_x / float(self.hackhz)
		self.mStart.y = mousePos.d_y / float(self.hackvz)
		self.mRect.setCorners(self.mStart, self.mStop)

	def clearSelection(self):
		shared.DPrint("SelectStuff",0,"Cleared all selections")
		for x in self.CurrentSelection:
			unitID=int(split(x.getName(),"_")[1])
			shared.unitHandeler.Get(unitID)._deselected()
		self.CurrentSelection=[]

	def endSelection(self):
		self.performSelection(self.mStart, self.mStop)
		self.mSelecting = False
		self.mRect.setVisible(False)
		self.LMBSel=False

	def performSelection(self, vec2first, vec2second):
		# I am the one who makes everything ready before you may start selecting stuff
		left =  vec2first.x
		right = vec2second.x
		top = vec2first.y
		bottom = vec2second.y
 
		if left > right:
			left, right = right, left
 
		if top > bottom:
			top, bottom = bottom, top
 
		if (right - left) * (bottom - top) < 0.001:
			self.mSelecting = False
			self.mRect.setVisible(False)
			self.LMBSel=False
			self.LMBFuck=False
			self.selectevent(None)
			shared.DPrint("SelectStuff",0,"Selection: Selection Too Small")

 		else:
			## Rays
			topLeft     = self.camera.camera.getCameraToViewportRay(left, top)
			topRight    = self.camera.camera.getCameraToViewportRay(right, top)
			bottomLeft  = self.camera.camera.getCameraToViewportRay(left, bottom)
			bottomRight = self.camera.camera.getCameraToViewportRay(right, bottom);
	 
	 
			vol = ogre.PlaneBoundedVolume()
			planeList = vol.planes
			p = ogre.Plane(  topLeft.getPoint(3),
							 topRight.getPoint(3),
							 bottomRight.getPoint(3))
			p2 = ogre.Plane( topLeft.getOrigin(),
							 topLeft.getPoint(100),
							 topRight.getPoint(100))
			p3 = ogre.Plane( topLeft.getOrigin(),
							 bottomLeft.getPoint(100),
							 topLeft.getPoint(100))
			p4 = ogre.Plane( bottomLeft.getOrigin(),
							 bottomRight.getPoint(100),
							 bottomLeft.getPoint(100))
			p5 = ogre.Plane( topRight.getOrigin(),
							 topRight.getPoint(100),
							 bottomRight.getPoint(100))
	 
			vol.planes.append(p)  ## front plane
			vol.planes.append(p2) ## top plane
			vol.planes.append(p3) ## left plane
			vol.planes.append(p4) ## bottom plane
			vol.planes.append(p5) ## right plane
	 
	 
			## These planes have now defined an "open box" which extends to infinity in front of the
			## camera. You can think of the rectangle we drew with the mouse as being the termination
			## point of the box just in front of the camera. 
			## Now that we have created the planes, we need to execute the query:
	 
			volList = ogre.PlaneBoundedVolumeList()
			volList.append(vol)
	 
			self.mVolQuery.setVolumes(volList)
	 
			if 1==1:
				self.mVolQuery.execute( self.querylistener )
			else:
	 
				print "=================="
				print "THIS CRASHES"
				print "=================="
	 
				for queryResult in self.mVolQuery.execute():
					if queryResult.movableObject is not None:
						selfect(queryResult.movableObject)

	def selectevent(self, evt):
		# I get called each time you click on an unit, ( Not when you drag a box over them )
		mousePos = MouseCursor.getSingleton().getPosition()
		mouseRay = self.camera.camera.getCameraToViewportRay(mousePos.d_x / float(self.hackhz),
													  mousePos.d_y / float(self.hackvz))
		self.raySceneQuery.setRay(mouseRay)
		self.raySceneQuery.setSortByDistance(True)
		result = self.raySceneQuery.execute()
		if len(result) > 0:
			for item in result:
				if item.movable and item.movable.getName()[0:5] != "tile[" and item.movable.getName()!= "Camera" and item.movable.getParentSceneNode().getName()[:8]=="unitNode":
					foosel=[]
					for x in self.CurrentSelection:
						if x.getName() == item.movable.getParentSceneNode().getName():
							foosel.append(x)
							shared.DPrint("SelectStuff",0,"Selected: "+x.getName())
					if len(foosel)==0:
						unitID=int(split(item.movable.getParentSceneNode().getName(),"_")[1])
						shared.unitHandeler.Get(unitID)._selected()
						self.CurrentSelection.append(item.movable.getParentSceneNode())
					for x in foosel:
						unitID=int(split(item.movable.getParentSceneNode().getName(),"_")[1])
						shared.unitHandeler.Get(unitID)._deselected()
						del self.CurrentSelection[self.CurrentSelection.index(x)]
					foosel=[]
					#print(self.CurrentSelection)
					#print("_____________________________________")
					shared.DirectorManager.SelectedEvent(self.CurrentSelection)

					break # We found an existing object
				elif item.worldFragment:
					shared.DPrint("SelectStuff",0,"Selection: World Selected")
		if len(self.CurrentSelection):
			for x in self.CurrentSelection:
				#x.showBoundingBox(True)
				print(x.getName())

	def actionClick(self, mX, mY):
		# I get called each time you rightclick on the terrain, or over an unit
		mouseRay=self.camera.camera.getCameraToViewportRay(mX, mY)
		self.raySceneQuery.setRay(mouseRay)
		self.raySceneQuery.setSortByDistance(True)
		result=self.raySceneQuery.execute()
		if len(result)>0:
			for item in result:
				if item.movable and item.movable.getParentSceneNode().getName()[:8]=="unitNode":
					unitID=int(split(item.movable.getParentSceneNode().getName(),"_")[1])
					unitRclicked=shared.unitHandeler.Get(unitID)
					shared.DirectorManager.ActionEvent(unitRclicked)
					break

				elif item.movable and item.movable.getName()[0:5] == "tile[":
					#item.movable.getParentSceneNode().showBoundingBox(True)
					res2=mouseRay.intersects(item.movable.getWorldBoundingBox())
					posRclicked=mouseRay.getPoint(res2.second)
					ClickPosition=(posRclicked[0],posRclicked[1],posRclicked[2])
					#Decal=TerrainMDecal() #posRclicked,200, "rnad", True
					#TerrainMDecal.makeMaterialReceiveDecal(item.movable.getMaterialName())
					#Ent=shared.EntityHandeler.Create(8000+randrange(1,100), "robot", "No")
					#Decal.SetPos(0, 0, 10, 9999999)
					#Ent.SetPosition(posRclicked[0],posRclicked[1],posRclicked[2])
					# if self.TestStuff:
					# 	self.Decal.SetPosition(DecalPlace)
					# else:
					# 	self.Decal=shared.DecalManager.Create("MCircle", DecalPlace, (270,0,0))
					# 	self.TestStuff=True
					# break
					
					#shared.WaypointManager.Show(0, DecalPlace)
					#debug.RCC("dirgo "+str(floor(DecalPlace[0]))+" "+str(floor(DecalPlace[2])))

					shared.DirectorManager.MovementEvent(ClickPosition)

					break
					

class SelectionRectangle(ogre.ManualObject):
	# I am the visual reprensation of the selection box
	##===============================================================================##
	##   Selection Rectangle Class
	##===============================================================================##
	def __init__(self,name):
		## set selection rectangle to render in 2D and it sits on top of all other objects on screen
		## ( render when Ogre's Overlays render)
		ogre.ManualObject.__init__(self,name)
		self.setRenderQueueGroup(ogre.RenderQueueGroupID.RENDER_QUEUE_OVERLAY)
		self.setUseIdentityProjection(True)
		self.setUseIdentityView(True)
		self.setQueryFlags(0)
 
	def setCorners(self, vecFirst, vecSecond):
		## Sets the corners of the SelectionRectangle.  Every parameter should be in the
		## range [0, 1] representing a percentage of the screen the SelectionRectangle
		## should take up.
		self._setCorners(vecFirst.x, vecFirst.y, vecSecond.x, vecSecond.y)

	def _setCorners(self, left, top, right, bottom):
		## CEGUI mouse cursor defines the top of the screen at 0, the bottom at 1. 
		## Convert these to numbers in the range [-1, 1], in our new coordinate system, 
		## the top of the screen is +1, the bottom is -1
		left = left * 2 - 1
		right = right * 2 - 1
		top = 1 - top * 2
		bottom = 1 - bottom * 2
		## create our rectangle, we will define 5 points (the first and the last point 
		## are the same to connect the entire rectangle)
		self.clear()
		self.begin("", ogre.RenderOperation.OT_LINE_STRIP)
		self.position(left, top, -1)
		self.position(right, top, -1)
		self.position(right, bottom, -1)
		self.position(left, bottom, -1)
		self.position(left, top, -1)
		self.end()
		# set the bounding box of the object to be infinite, so that the camera will 
		# always be inside of it
		box = ogre.AxisAlignedBox()
		box.setInfinite()
		self.setBoundingBox(box)
 
class PlaneQueryListener(ogre.SceneQueryListener):
	# I get called each time you multiselect stuff, aka. if you drag a box over units 
	##===============================================================================##
	##   Subclassed Scene Query Listener
	##===============================================================================##
	#""" the listener that gets called for each pair of intersecting objects """   
	def __init__ (self, SelStf):
		ogre.SceneQueryListener.__init__ ( self )
		self.SelStf=SelStf
 
	def queryResult (  self, firstMovable):
		if firstMovable and firstMovable.getName()[0:5] != "tile[" and firstMovable.getName()!= "Camera" and firstMovable.getParentSceneNode().getName()[:8]=="unitNode":
			foosel=[]
			for x in self.SelStf.CurrentSelection:
				if x.getName() == firstMovable.getParentSceneNode().getName():
					foosel.append(x)
					#print(foosel.gert)
			if len(foosel)==0:
				unitID=int(split(firstMovable.getParentSceneNode().getName(),"_")[1])
				shared.unitHandeler.Get(unitID)._selected()
				self.SelStf.CurrentSelection.append(firstMovable.getParentSceneNode())
			for x in foosel:
				unitID=int(split(firstMovable.getParentSceneNode().getName(),"_")[1])
				shared.unitHandeler.Get(unitID)._deselected()
				del self.SelStf.CurrentSelection[self.SelStf.CurrentSelection.index(x)]
			foosel=[]

			shared.DirectorManager.SelectedEvent(self.SelStf.CurrentSelection)

			#print(self.SelStf.CurrentSelection)
			#print("_____________________________________")
			#print type(firstMovable)
			#print firstMovable.name, dir(firstMovable)
			if len(self.SelStf.CurrentSelection):
				for x in self.SelStf.CurrentSelection:
					#x.showBoundingBox(True)
					#print(x.getName())
					pass
		return True
	