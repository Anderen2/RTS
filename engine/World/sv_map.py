#sv_map
#ServerSided Map

import pickle
from time import sleep
from engine import shared, debug
from PIL import Image
from string import split

class MapLoader():
	def __init__(self):
		global MAPLOADERVERSION
		MAPLOADERVERSION=1.0
		shared.DPrint("Maploader", 0, "Initializing..")
		debug.ACC("map", self.Load, info="Load a map\nUsage: map mapfile. ex. map nice.map")

		self.MediaPlacement = shared.wd+"media/materials/textures/"

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
		#Setup Terrain
		TerrainHeightmap = terraincfg["Heightmap"]["Heightmap File"]
		TerrainScale = terraincfg["Heightmap"]["Size"]
		TerrainHeight = terraincfg["Heightmap"]["Height"]
		TerrainInstance = Terrain(self.MediaPlacement + TerrainHeightmap, TerrainScale, TerrainHeight)

		if terraincfg["Water"]["Type"]!="None":
			WaterAltitude = terraincfg["Water"]["Altitude"]
			WaterType = terraincfg["Water"]["Type"]
			WaterInstance = Water(WaterAltitude, WaterType)
		else:
			WaterInstance=None

		return TerrainInstance, WaterInstance

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
		self.Terrain, self.Water = shared.MapLoader.terrainLoad(self.config["Terrain"])

		#Setup Decoratiors
		# for ID, Content in self.config["Decorator"].iteritems():
		# 	name=self.config["Decorator"][ID]["name"]
		# 	pos=self.config["Decorator"][ID]["pos"]
		# 	rot=self.config["Decorator"][ID]["rot"]

		# 	shared.DPrint("Map", 0, "Placing decorator: "+name+" ("+str(ID)+")"+" @ "+str(pos))
		# 	shared.decHandeler.Create(name, pos).entity.setOrientation(rot[0], rot[1], rot[2], rot[3])

		if shared.Pathfinder:
			ACCURACY = 100
			tmp = split(self.mapname, ".")
			NavFile = "Data/Map/"+".".join(tmp[0:len(tmp)-1])+".nav"

			if shared.Pathfinder.aStarPath.Load(self.config["Terrain"]["Heightmap"]["Size"], ACCURACY, NavFile):
				shared.DPrint("Map", 0, "Astar Grid Nodes successfully loaded from .nav file: "+str(NavFile))
			else:
				shared.DPrint("Map", 0, "Astar Grid Nodes could not be loaded from .nav file: "+str(NavFile))
				shared.DPrint("Map", 0, "Generating new aStar Grid.. Please Wait..")
				##GENERATE NEW GRID AND SAVE IT HERE!

		shared.PlayerManager.SetupMapUnits(self.config["Units"])

class Terrain():
	def __init__(self, filepath, scale, height):
		self.TerrainImagePath = filepath
		self.TerrainScale = scale
		self.TerrainHeight = height
		#self.TerrainHeight = 200

		self.TerrainFile = Image.open(filepath)
		self.TerrainImage = self.TerrainFile.load()

		self.grayres = self.TerrainFile.getextrema()
		self.imgfact = self.TerrainFile.size[0]/float(100)
		self.mapfact = float(self.TerrainScale)/float(100)
		self.altfact = float(self.TerrainHeight)

	def getHeightAtPos(self, x, y):
		lx = (((float(x)/float(self.TerrainScale))*self.imgfact)*100)-1
		ly = (((float(y)/float(self.TerrainScale))*self.imgfact)*100)-1
		print("Requested: ",(x,y))
		print("Locals: ",(lx, ly))
		try:
			print(float(self.TerrainImage[lx,ly])/self.grayres[1]*self.altfact)
			print("TImg: %f", (float(self.TerrainImage[lx,ly])))
			print("GRes:   ", (self.grayres))
			print("Fact: %f", (self.altfact))
			#return (float(self.TerrainImage[lx,ly] + (self.grayres[0] - 16384))/self.grayres[1]*self.altfact)
			return float(self.TerrainImage[lx,ly])/65535*self.altfact #Figure what the fuck that is going on here (HARDCODE)
		except IndexError:
			return 0

class Water():
	def __init__(self, Altitude, WaterType):
		self.Altitude = Altitude
		self.WaterType = WaterType

	def getIfInWater(self, x, y):
		if shared.Map.Terrain.getHeightAtPos(x, y)<self.Altitude:
			return True
		else:
			return False
