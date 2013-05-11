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
		properties=pickle.loads(mapfile.read())
		if float(properties["map"]["mapfilev"])<MAPLOADERVERSION:
			shared.DPrint("Maploader", 2, "Map is an older version than the importer, errors may occur!")

		return Map(properties)

class Map():
	def __init__(self, properties):
		self.properties=properties
		self.name=properties["map"]["name"]
		self.version=properties["map"]["version"]

		shared.DPrint("Map", 0, "Map "+self.name+" Initialized")

	def Setup(self):
		shared.DPrint("Map", 0, "Starting to setup scene according to mapfile")

		## TERRAIN TO render3d
		## Player/Camera TO Playermanager
		## Decorations to DecorationManager
		## Units to UnitManager
		## Zones to ZoneManager

		#Decoratorplacer
		for x in self.properties["decos"]:
			name=self.properties["decos"][x]["name"]

			pos=self.properties["decos"][x]["xyz"]
			posl=pos.split(",")
			rot=self.properties["decos"][x]["rot"]
			rotl=rot.split(",")
			shared.DPrint("Map", 0, "Placing decorator: "+name+" ("+x+")"+" @ "+pos)
			shared.decHandeler.Create(name, posl, rotl)