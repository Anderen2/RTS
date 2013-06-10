#Mapfile Creator

from engine import shared, debug
import pickle

class Mapfile():
	"""This class defines the map, and all changes to the map from the mapeditor will be saved here. This allows us to easily dump it to a file later"""
	def __init__(self):
		self.MapConfig={}
		self.TerrainConfig={}
		self.DecoratorConfig={}

	def Generate(self):
		for ID, Deco in shared.decHandeler.decorators.iteritems():
			pos=Deco.entity.node.getPosition()
			rot=(float(Deco.entity.node.getOrientation().getRoll().valueDegrees()), float(Deco.entity.node.getOrientation().getPitch().valueDegrees()), float(Deco.entity.node.getOrientation().getYaw().valueDegrees()))

			self.DecoratorConfig[ID]={}
			self.DecoratorConfig[ID]["pos"]=(pos.x, pos.y, pos.z)
			self.DecoratorConfig[ID]["rot"]=rot
			self.DecoratorConfig[ID]["name"]=Deco.name

		self.Map={"Map": self.MapConfig, "Terrain": self.TerrainConfig, "Decorator": self.DecoratorConfig}

	def Save(self, filename):
		self.Generate()
		File=open(filename,"w")
		pickle.dump(self.Map, File)