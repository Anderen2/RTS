#Ground Context Options

from engine import debug, shared
from engine.Lib import textvalidator
from engine.Tool.Mapeditor import popupgui

import ogre.renderer.OGRE as ogre
from ogre.gui.CEGUI import MouseCursor

class contextGround():
	def __init__(self):
		#Raytrace
		self.raySceneQuery = shared.render3dScene.sceneManager.createRayQuery(ogre.Ray())
		self.dimh, self.dimv = shared.render3dCamera.getDimensions()
		
		self.options=["Add decorator", "Add unit", "Add effect", "Terrain settings", "Map settings"]
		self.optfunc=[self.sDec, self.sUnit, self.sEff, self.sTerrain, self.sMap]

	def sDec(self):
		print("Pavin' ground")
		self.Position=self.getClickedPos()
		shared.globalGUI.SSearch.ask("decorators", self.rDec)

	def rDec(self, result):
		shared.decHandeler.Create(result, pos=self.Position)

	def sUnit(self):
		pass

	def sEff(self):
		pass

	def sTerrain(self):
		layout={"Heightmap":{"Heightmap File":"file","Scale":"vector2","Height":"float", "TileSize":"int", "PageSize":"int"}, "Texture":{"Base Texture":"file", "Alpha Splatmaps":"filelist", "Alpha SplatTextures": "filelist"}, "Water":{"Type":["Ocean", "None"], "Altitude":"float"}, "Lightning":{"Position of sun":"vector3", "Ambient":"color"}}
		
		config=shared.Mapfile.TerrainConfig

		shared.globalGUI.OptionsGUI.ask("Terrain Settings", self.callbackTerrain, layout, config)

	def sMap(self):
		layout={"General": {"Name":"str", "Version":"float", "Description":"str"}, "Players":{"Count": "int"}}

		config=shared.Mapfile.MapConfig
		shared.globalGUI.OptionsGUI.ask("Map Settings", self.callbackMap, layout, config)

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

	def callbackTerrain(self, config):
		shared.Mapfile.TerrainConfig=textvalidator.convertConfig(config)

		for section, keys in config.iteritems():
			print("["+section+"]")

			for key, value in keys.iteritems():
				print(key+"="+str(value))

		shared.MapLoader.terrainLoad(textvalidator.convertConfig(config))

	def callbackMap(self, config):
		for section, keys in config.iteritems():
			print("["+section+"]")

			for key, value in keys.iteritems():
				print(key+"="+str(value))

		shared.Mapfile.MapConfig=textvalidator.convertConfig(config)