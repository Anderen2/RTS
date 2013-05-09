#Mapfile loader
import pickle
from engine import shared, debug

MAPLOADERVERSION=1.0

def Init():
	shared.DPrint("Maploader", 0, "Initializing..")

def Load(mapname):
	global MAPLOADERVERSION
	shared.DPrint("Maploader", 0, "Loading map: "+mapname)
	mapfile=open("Data/Map/"+mapname, "r")
	properties=pickle.loads(mapfile.read())
	if float(properties["mapfilev"])<MAPLOADERVERSION:
		shared.DPrint("Maploader", 2, "Map is an older version than the importer, errors may occur!")

	return Map(properties)

class Map():
	def __init__(self, properties):
		self.properties=properties
		self.name=properties["name"]
		self.version=properties["version"]

		shared.DPrint("Map", 0, "Map "+self.name+" Initialized")

	def Setup(self):
		shared.DPrint("Map", 0, "Starting to setup scene according to mapfile")

		## TERRAIN TO render3d
		## Player/Camera TO Playermanager
		## Decorations to DecorationManager
		## Units to UnitManager
		## Zones to ZoneManager
		