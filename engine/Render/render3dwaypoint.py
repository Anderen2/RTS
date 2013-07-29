#Render3dExtension - render3dwaypoint
#Classes for handeling Waypoints
#Highlevel Module (Decals + Entitys)

from engine import shared, debug
from engine.shared import DPrint
import render3dshapes as Shape
from ogre.renderer.OGRE import Degree, RENDER_QUEUE_SKIES_LATE, RENDER_QUEUE_BACKGROUND

class WaypointManager():
	def __init__(self):
		self.waypoints=[]
		self.waypointPathEnt=None
		self.waypointPathNumber=0

	def Load(self):
		self.MoveWaypointShape=Shape.Tetra("Move", "blah", 20, True)

	def Create(self, pos, waypointType, fade):
		wp = Waypoint(len(self.waypoints), pos, waypointType, fade)
		self.waypoints.append(wp)
		return wp

	def update(self, group, wpdata):
		if group!=None:
			self.clearAllWaypoints()
			for waypointType, position in wpdata:
				if waypointType!=None and position!=None:
					print(waypointType, position)
					self.Create(position, waypointType, False)

			if len(self.waypoints)>1:
				self.drawPath()
			else:
				if self.waypointPathEnt!=None:
					self.waypointPathNode.detachObject(self.waypointPathEnt)
					shared.render3dScene.sceneManager.destroyEntity(self.waypointPathEnt)
					shared.render3dScene.sceneManager.destroySceneNode(self.waypointPathNode)
					self.waypointPathEnt = None
		else:
			self.clearAllWaypoints()
			if self.waypointPathEnt!=None:
				self.waypointPathNode.detachObject(self.waypointPathEnt)
				shared.render3dScene.sceneManager.destroyEntity(self.waypointPathEnt)
				shared.render3dScene.sceneManager.destroySceneNode(self.waypointPathNode)
				#self.waypointPath.unload()
				self.waypointPathEnt = None

	def clearAllWaypoints(self):
		for waypoint in self.waypoints:
			waypoint.Delete()
		self.waypoints=[]

	def Remove(self, Waypoint):
		self.waypoints.remove(Waypoint)

	def drawPath(self):
		if self.waypointPathEnt!=None:
			self.waypointPathNode.detachObject(self.waypointPathEnt)
			shared.render3dScene.sceneManager.destroyEntity(self.waypointPathEnt)
			shared.render3dScene.sceneManager.destroySceneNode(self.waypointPathNode)
			self.waypointPathEnt = None

		pathlist=[]
		for waypoint in self.waypoints:
			pathlist.append((waypoint.node.getPosition().x, waypoint.node.getPosition().y, waypoint.node.getPosition().z))
		#print pathlist
		self.waypointPath = Shape.Path("WaypointPath"+str(self.waypointPathNumber), "BaseWhiteNoLighting", pathlist, Mesh=True)
		##print(self.waypointPath)
		self.waypointPathEnt = shared.render3dScene.sceneManager.createEntity("WaypointPath", "WaypointPath"+str(self.waypointPathNumber))
		##print(self.waypointPathEnt)
		self.waypointPathNode = shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode("WaypointPath")
		self.waypointPathNode.attachObject(self.waypointPathEnt)

		self.waypointPathNumber+=1


class Waypoint():
	def __init__(self, WID, pos, waypointtype, fade):
		self.WID = WID
		self.ent=shared.render3dScene.sceneManager.createEntity("Waypoint"+str(self.WID), waypointtype)
		self.node=shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode("Waypoint"+str(self.WID))
		self.node.attachObject(self.ent)
		self.node.rotate((1,0,0),Degree(180))
		self.decal=shared.DecalManager.Create(waypointtype,(-300,-300,-300),(270,0,0))
		
		self.node.setPosition((pos[0],pos[1]+50,pos[2]))
		self.decal.SetPosition((pos[0],pos[1]+1,pos[2]+25))
		self.decal.ent.setRenderQueueGroup(RENDER_QUEUE_SKIES_LATE)

	def Delete(self):
		print("Waypoint: Detaching node")
		self.node.detachObject(self.ent)
		print("Waypoint: Deleting Entity")
		shared.render3dScene.sceneManager.destroyEntity(self.ent)
		print("Waypoint: Deleting Node")
		shared.render3dScene.sceneManager.destroySceneNode(self.node)