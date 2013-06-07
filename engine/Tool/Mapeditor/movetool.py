#New Selection written from scratch
#Used to move stuff in the map manager

import ogre.renderer.OGRE as ogre
from ogre.gui.CEGUI import MouseCursor

from engine import debug, shared

class MoveTool():
	def __init__(self):
		#Raytrace
		self.raySceneQuery = shared.render3dScene.sceneManager.createRayQuery(ogre.Ray())

		self.dimh, self.dimv = shared.render3dCamera.getDimensions()

		self.CurrentHold=None

	def MousePressed(self, id):
		print("Raybeens")
		mousePos = MouseCursor.getSingleton().getPosition()
		mouseRay = shared.render3dCamera.camera.getCameraToViewportRay(mousePos.d_x / float(self.dimh),
													  mousePos.d_y / float(self.dimv))
		self.raySceneQuery.setRay(mouseRay)
		self.raySceneQuery.setSortByDistance(True)
		result = self.raySceneQuery.execute()
		if len(result)>0:
			for item in result:
				if item.movable and item.movable.getName()!="Camera" and item.movable.getName()[0:5] != "tile[":
					print "____________________________________"
					print item.movable.getName()
					print item.movable.getParentSceneNode().getName()

					if "-" in item.movable.getName():
						#If there is a dash in the scenenode name, it means that the currently selected entity is a subentity to something else
						#Ex. the turret on top of the tank
						print(item.movable.getName())
						print(item.movable.getParentSceneNode().getName())
						print(item.movable.getParentSceneNode().getParentSceneNode().getName())
						shared.DPrint("movetool", 3, "This is not supported!")
						#self.CurrentHold=shared.decHandeler.Get(int(item.movable.getParentSceneNode().getParentSceneNode().getName()[4:]))
					else:
						self.CurrentHold=shared.decHandeler.Get(int(item.movable.getName()[4:]))

					if self.CurrentHold!=None:
						self.CurrentHold.entity.node.showBoundingBox(True)

					break

	def MouseReleased(self, id):
		print("Raybeens II")
		if self.CurrentHold!=None:
			self.CurrentHold.entity.node.showBoundingBox(False)
		self.CurrentHold=None

	def MouseMoved(self, X, Y):
		if self.CurrentHold!=None:
			mousePos = MouseCursor.getSingleton().getPosition()
			mouseRay = shared.render3dCamera.camera.getCameraToViewportRay(mousePos.d_x / float(self.dimh),
														  mousePos.d_y / float(self.dimv))
			self.raySceneQuery.setRay(mouseRay)
			result = self.raySceneQuery.execute()
			if len(result)>0:
				for item in result:
					if item.movable and item.movable.getName()[0:5] == "tile[":
						hitpoint=mouseRay.intersects(item.movable.getWorldBoundingBox())
						posMoved=mouseRay.getPoint(hitpoint.second)
						MovePosition=(posMoved[0],posMoved[1],posMoved[2])
						YOffset=self.CurrentHold.entity.node._getWorldAABB().getHalfSize().y
						self.CurrentHold.entity.SetPosition(posMoved[0],posMoved[1]+YOffset,posMoved[2])
						break