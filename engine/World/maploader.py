#Mapfile loader
import pickle
from engine import shared, debug

class MapLoader():
	def __init__(self):
		global MAPLOADERVERSION
		MAPLOADERVERSION=1.0
		shared.DPrint("Maploader", 0, "Initializing..")

	def Load(self, mapname):
		global MAPLOADERVERSION
		shared.DPrint("Maploader", 0, "Loading map: "+mapname)
		mapfile=open("Data/Map/"+mapname, "r")
		mapconfig=pickle.loads(mapfile.read())
		if float(mapconfig["Map"]["General"]["Version"])<MAPLOADERVERSION:
			shared.DPrint("Maploader", 2, "Map is an older version than the importer, errors may occur!")

		return Map(mapconfig)

	def terrainLoad(self, terraincfg):
		self.createTerrainCFG(terraincfg)
		shared.render3dScene.RldTerrain()

		if terraincfg["Water"]["Type"]!="None":
			terrainX=float(terraincfg["Heightmap"]["Scale"][0])
			terrainY=float(terraincfg["Heightmap"]["Scale"][1])
			if len(shared.WaterManager.waters)==0:
				shared.WaterManager.Create((terrainX/2, float(terraincfg["Water"]["Altitude"]), terrainY/2), terrainX, terrainY)
			else:
				shared.WaterManager.waters[0].node.setPosition((terrainX/2, float(terraincfg["Water"]["Altitude"]), terrainY/2))
		else:
			if len(shared.WaterManager.waters)==0:
				shared.WaterManager.waters[0].destroy()

	def createTerrainCFG(self, terraincfg):
		Comment="# Automaticly generated from current map. Do NOT mod this file manually, your changes will only be overwritten!"
		PageSource="Heightmap"
		HeightmapImage=terraincfg["Heightmap"]["Heightmap File"]
		PageSize=str(terraincfg["Heightmap"]["PageSize"])
		TileSize="129"
		MaxPixelError="30000"
		PageWorldX=str(terraincfg["Heightmap"]["Scale"][0])
		PageWorldZ=str(terraincfg["Heightmap"]["Scale"][1])
		MaxHeight=str(terraincfg["Heightmap"]["Height"])
		MaxMipMapLevel="5"
		LODMorphStart="0.05"
		CustomMaterialName="Template/Terrain"

		cfgBuffer=Comment+"\nPageSource="+PageSource+"\nHeightmap.image="+HeightmapImage+"\nPageSize="+PageSize+"\nTileSize="+TileSize+"\nMaxPixelError="+MaxPixelError+"\nPageWorldX="+PageWorldX+"\nPageWorldZ="+PageWorldZ+"\nMaxHeight="+MaxHeight+"\nMaxMipMapLevel="+MaxMipMapLevel+"\nLODMorphStart="+LODMorphStart+"\n# YARTS Autoconfig End\n"

		cfgFile=open("./media/terrain2.cfg", "w")
		cfgFile.write(cfgBuffer)
		cfgFile.flush()
		cfgFile.close()

class Map():
	def __init__(self, mapfile):
		self.config=mapfile
		self.name=self.config["Map"]["General"]["Name"]
		self.version=self.config["Map"]["General"]["Version"]
		self.description=self.config["Map"]["General"]["Description"]
		self.maxplayers=self.config["Map"]["Players"]["Count"]

		shared.DPrint("Map", 0, "Map "+self.name+" Initialized")

	def Setup(self):
		shared.DPrint("Map", 0, "Starting to setup scene according to mapfile")

		## TERRAIN TO render3d
		## Player/Camera TO Playermanager
		## Decorations to DecorationManager
		## Units to UnitManager
		## Zones to ZoneManager

		# #Decoratorplacer
		# for x in self.properties["decos"]:
		# 	name=self.properties["decos"][x]["name"]

		# 	pos=self.properties["decos"][x]["xyz"]
		# 	posl=pos.split(",")
		# 	rot=self.properties["decos"][x]["rot"]
		# 	rotl=rot.split(",")
		# 	shared.DPrint("Map", 0, "Placing decorator: "+name+" ("+x+")"+" @ "+pos)
		# 	shared.decHandeler.Create(name, posl, rotl)

		#Setup Terrain (Heightmap, Water and Textures)
		shared.MapLoader.terrainLoad(self.config["Terrain"])

		#Setup Decoratiors
		for ID, Content in self.config["Decorator"].iteritems():
			name=self.config["Decorator"][ID]["name"]
			pos=self.config["Decorator"][ID]["pos"]
			rot=self.config["Decorator"][ID]["rot"]

			shared.DPrint("Map", 0, "Placing decorator: "+name+" ("+str(ID)+")"+" @ "+str(pos))
			shared.decHandeler.Create(name, pos, rot)