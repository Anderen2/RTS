#Mapfile loader
import pickle
from engine import shared, debug

class MapLoader():
	def __init__(self):
		global MAPLOADERVERSION
		MAPLOADERVERSION=1.0
		shared.DPrint("Maploader", 0, "Initializing..")
		debug.ACC("map", self.Load, info="Load a map\nUsage: map mapfile. ex. map nice.map")

	def Load(self, mapname):
		global MAPLOADERVERSION
		shared.DPrint("Maploader", 0, "Loading map: "+mapname)
		mapfile=open("Data/Map/"+mapname, "r")
		mapconfig=pickle.loads(mapfile.read())
		if float(mapconfig["Map"]["General"]["Version"])<MAPLOADERVERSION:
			shared.DPrint("Maploader", 2, "Map is an older version than the importer, errors may occur!")

		self.Map=Map(mapconfig)
		return self.Map

	def terrainLoad(self, terraincfg):
		self.createTerrainCFG(terraincfg)

		#Create a dictionary with textures and alphamaps
		splattingDict = {}

		i=0
		for x in terraincfg["Texture"]["Alpha Splatmaps"]:
			Fun = x.replace("[", "").replace("]", "").replace(" ", "")
			splattingDict[terraincfg["Texture"]["Alpha SplatTextures"][i].replace("[", "").replace("]", "").replace(" ", "")]=Fun
			i+=1

		shared.render3dScene.createTerrainMaterial(terraincfg["Texture"]["Base Texture"], splattingDict)
		shared.render3dScene.RldTerrain()

		if terraincfg["Water"]["Type"]!="None":
			terrainX=int(terraincfg["Heightmap"]["Scale"][0])
			terrainY=int(terraincfg["Heightmap"]["Scale"][1])
			if len(shared.WaterManager.waters)==0:
				shared.WaterManager.Create((terrainX/2, int(terraincfg["Water"]["Altitude"]), terrainY/2), terrainX, terrainY)
			else:
				if (shared.WaterManager.waters[0].node.getPosition().x)/2==terrainX/2:
					shared.WaterManager.waters[0].node.setPosition((terrainX/2, int(terraincfg["Water"]["Altitude"]), terrainY/2))
				else:
					shared.WaterManager.Remove(0)
					shared.WaterManager.Create((terrainX/2, int(terraincfg["Water"]["Altitude"]), terrainY/2), terrainX, terrainY)
		else:
			if len(shared.WaterManager.waters)!=0:
				shared.WaterManager.Remove(0)

		if shared.FowManager!=None:
			if shared.FowManager.created==False:
				shared.FowManager.Create(int(terraincfg["Heightmap"]["Scale"][0]), int(terraincfg["Heightmap"]["Scale"][1]))

	def createTerrainCFG(self, terraincfg):
		Comment="# Automaticly generated from current map. Do NOT mod this file manually, your changes will only be overwritten!"
		PageSource="Heightmap"
		HeightmapImage=terraincfg["Heightmap"]["Heightmap File"]
		PageSize=str(terraincfg["Heightmap"]["PageSize"])
		TileSize=str(terraincfg["Heightmap"]["TileSize"])
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

		#Setup Terrain (Heightmap, Water and Textures)
		shared.MapLoader.terrainLoad(self.config["Terrain"])

		#Setup Decoratiors
		for ID, Content in self.config["Decorator"].iteritems():
			name=self.config["Decorator"][ID]["name"]
			pos=self.config["Decorator"][ID]["pos"]
			rot=self.config["Decorator"][ID]["rot"]

			shared.DPrint("Map", 0, "Placing decorator: "+name+" ("+str(ID)+")"+" @ "+str(pos))
			shared.decHandeler.Create(name, pos).entity.setOrientation(rot[0], rot[1], rot[2], rot[3])