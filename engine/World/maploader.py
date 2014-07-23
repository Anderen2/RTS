#Mapfile loader
import pickle
from engine import shared, debug
from string import split

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

		self.Map=Map(mapname, mapconfig)
		return self.Map

	def terrainLoad(self, terraincfg):
		#Create the terrain config
		shared.render3dTerrain.createTerrainCFG(terraincfg)

		#Create a dictionary with textures and alphamaps
		splattingDict = {}

		i=0
		if terraincfg["Texture"]["Alpha Splatmaps"]!=None:
			for x in terraincfg["Texture"]["Alpha Splatmaps"]:
				Fun = x.replace("[", "").replace("]", "").replace(" ", "")
				splattingDict[terraincfg["Texture"]["Alpha SplatTextures"][i].replace("[", "").replace("]", "").replace(" ", "")]=Fun
				i+=1

		shared.render3dTerrain.LoadTerrain()
		shared.render3dTerrain.createTerrainMaterial(terraincfg["Texture"]["Base Texture"], splattingDict)

		if terraincfg["Water"]["Type"]!="None":
			#terrainX=int(terraincfg["Heightmap"]["Scale"][0])
			#terrainY=int(terraincfg["Heightmap"]["Scale"][1])
			terrainX = int(terraincfg["Heightmap"]["Size"])
			terrainY = int(terraincfg["Heightmap"]["Size"])
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
				shared.FowManager.Create(int(terraincfg["Heightmap"]["Size"]), int(terraincfg["Heightmap"]["Size"]), shared.render3dTerrain.TerrainMaterial)

class Map():
	def __init__(self, mapname, mapfile):
		self.mapname = mapname
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
			newdec = shared.decHandeler.Create(name, pos)
			print(newdec)
			print(newdec.entity)
			newdec.entity.setOrientation(rot[0], rot[1], rot[2], rot[3])

		#Setup A* Pathfinding
		if shared.Pathfinder:
			ACCURACY = 100 # GET/CALC THIS AUTOMATICLY (HARDCODE)
			tmp = split(self.mapname, ".")
			NavFile = "Data/Map/"+".".join(tmp[0:len(tmp)-1])+".nav"

			if shared.Pathfinder.aStarPath.Load(self.config["Terrain"]["Heightmap"]["Size"], ACCURACY, NavFile):
				shared.DPrint("Map", 0, "Astar Grid Nodes successfully loaded from .nav file: "+str(NavFile))
			else:
				shared.DPrint("Map", 0, "Astar Grid Nodes could not be loaded from .nav file: "+str(NavFile))
				shared.DPrint("Map", 0, "Generating new aStar Grid.. Please Wait..")
				##GENERATE NEW GRID AND SAVE IT HERE!