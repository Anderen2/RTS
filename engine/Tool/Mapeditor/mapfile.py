#Mapfile Creator

from engine import shared, debug
from twisted.internet import reactor
import pickle

class Mapfile():
	"""This class defines the map, and all changes to the map from the mapeditor will be saved here. This allows us to easily dump it to a file later"""
	def __init__(self):
		self.MapConfig={}
		self.TerrainConfig={}
		self.DecoratorConfig={}

		self.Load()

	def Generate(self):
		self.DecoratorConfig={}
		for ID, Deco in shared.decHandeler.decorators.iteritems():
			print (ID, Deco)
			pos=Deco.entity.node.getPosition()
			print(pos)
			rot=(float(Deco.entity.node.getOrientation().w), float(Deco.entity.node.getOrientation().x), float(Deco.entity.node.getOrientation().y), float(Deco.entity.node.getOrientation().z))

			self.DecoratorConfig[ID]={}
			self.DecoratorConfig[ID]["pos"]=(pos.x, pos.y, pos.z)
			self.DecoratorConfig[ID]["rot"]=rot
			self.DecoratorConfig[ID]["name"]=Deco.name

		self.Map={"Map": self.MapConfig, "Terrain": self.TerrainConfig, "Decorator": self.DecoratorConfig}

	def Save(self, filename):
		self.Generate()
		File=open(filename,"w")
		pickle.dump(self.Map, File)

	def Load(self):
		self.Map=shared.MapLoader.Map.config
		self.MapConfig=self.Map["Map"]
		self.TerrainConfig=self.Map["Terrain"]
		self.DecoratorConfig=self.Map["Decorator"]

	# def checkYourPrivileges(self):
	# 	if len(self.TerrainConfig)>1:
	# 		print(self.TerrainConfig["Heightmap"]["Scale"]+"test")
	# 	else:
	# 		print("Shit is cahs!")
	# 	#reactor.callLater(1, self.checkYourPrivileges)