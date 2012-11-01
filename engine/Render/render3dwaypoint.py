#Render3dExtension - render3dwaypoint
#Classes for handeling Waypoints
#Highlevel Module (Decals + Entitys)

from engine import shared, debug
from engine.shared import DPrint
import render3dshapes as Shape
from ogre.renderer.OGRE import Degree

class WaypointManager():
	def __init__(self):
		self.params={}

	def Load(self):
		#Moving Waypoint
		self.MoveWaypointShape=Shape.Tetra("MoveWaypoint", "blah", 20, True)
		self.MoveWaypointEnt=shared.render3dScene.sceneManager.createEntity("MoveWaypoint", "MoveWaypoint")
		self.MoveWaypointNode=shared.render3dScene.sceneManager.getRootSceneNode().createChildSceneNode("MoveWaypoint")
		self.MoveWaypointNode.rotate((1,0,0),Degree(180))
		self.MoveWaypointDecal=shared.DecalManager.Create("Move",(-300,-300,-300),(270,0,0))

	def Show(self, Type, pos):
		if Type==0:
			self.MoveWaypointNode.detachObject(self.MoveWaypointEnt)
			self.MoveWaypointNode.attachObject(self.MoveWaypointEnt)
			self.MoveWaypointNode.setPosition((pos[0],pos[1]+50,pos[2]))
			self.MoveWaypointDecal.SetPosition((pos[0],pos[1]+1,pos[2]+25))
			print(pos)

	def Hide(self, type):
		if Type==0:
			self.MoveWaypointNode.detachObject(self.MoveWaypointEnt)
			self.MoveWaypointDecal.SetPosition((-300,-300,-300))