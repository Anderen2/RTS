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

	def MousePressed(self):
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
						self.CurrentHold=shared.decHandeler.Get(int(item.movable.getParentSceneNode().getName()[4:]))
					else:
						self.CurrentHold=shared.decHandeler.Get(int(item.movable.getName()[4:]))
					break

	def MouseReleased(self):
		print("Raybeens II")
		mousePos = MouseCursor.getSingleton().getPosition()
		mouseRay = shared.render3dCamera.camera.getCameraToViewportRay(mousePos.d_x / float(self.dimh),
													  mousePos.d_y / float(self.dimv))
		self.raySceneQuery.setRay(mouseRay)
		result = self.raySceneQuery.execute()
		if len(result)>0:
			for item in result:
				if item.movable and item.movable.getName()[0:5] == "tile[":
					res2=mouseRay.intersects(item.movable.getWorldBoundingBox())
					posRclicked=mouseRay.getPoint(res2.second)
					ClickPosition=(posRclicked[0],posRclicked[1],posRclicked[2])
					print(ClickPosition)
					if self.CurrentHold!=None:
						self.CurrentHold.entity.SetPosition(posRclicked[0],posRclicked[1],posRclicked[2])
					self.CurrentHold=None
					break