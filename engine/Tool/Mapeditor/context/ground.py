#Ground Context Options

from engine import debug, shared
from engine.Tool.Mapeditor import popupgui

import ogre.renderer.OGRE as ogre
from ogre.gui.CEGUI import MouseCursor

class contextGround():
	def __init__(self):
		#Raytrace
		self.raySceneQuery = shared.render3dScene.sceneManager.createRayQuery(ogre.Ray())
		self.dimh, self.dimv = shared.render3dCamera.getDimensions()
		
		self.options=["Add decorator", "Add unit", "Add effect", "Terrain settings", "Water settings", "Map settings"]
		self.optfunc=[self.sDec, self.sUnit, self.sEff, self.sTerrain, self.sWater, self.sMap]

	def sDec(self):
		print("Pavin' ground")
		self.Position=self.getClickedPos()
		shared.globalGUI.SSearch.ask("Entlist", self.rDec)

	def rDec(self, result):
		shared.decHandeler.Create(result, pos=self.Position)

	def sUnit(self):
		pass

	def sEff(self):
		pass

	def sTerrain(self):
		pass

	def sWater(self):
		pass

	def sMap(self):
		pass

	def getClickedPos(self):
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
					Position=(posMoved[0],posMoved[1],posMoved[2])
					return Position
					break