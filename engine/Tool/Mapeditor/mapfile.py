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
		self.UnitConfig={}

		self.Load()

	def Generate(self):
		#Decorators
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

		#Units
		self.UnitConfig={}
		for ID, Unit in shared.decHandeler.customDecos["unit"]["decos"].iteritems():
			print (ID, Unit)
			pos=Unit.entity.node.getPosition()
			print(pos)
			rot=(float(Unit.entity.node.getOrientation().w), float(Unit.entity.node.getOrientation().x), float(Unit.entity.node.getOrientation().y), float(Unit.entity.node.getOrientation().z))
			pidowner = Unit._mapeditorValues["pidowner"]
			attribs = Unit._mapeditorValues["attribs"]
			entname = Unit.name

			self.UnitConfig[ID]={}
			self.UnitConfig[ID]["name"]=Unit._mapeditorValues["name"]
			self.UnitConfig[ID]["ent"]=entname
			self.UnitConfig[ID]["pos"]=(pos.x, pos.y, pos.z)
			self.UnitConfig[ID]["rot"]=rot
			self.UnitConfig[ID]["pid"]=pidowner
			self.UnitConfig[ID]["attribs"]=attribs

		self.Map={"Map": self.MapConfig, "Terrain": self.TerrainConfig, "Decorator": self.DecoratorConfig, "Units": self.UnitConfig}

	def Save(self, filename):
		self.Generate()
		File=open(filename,"w")
		pickle.dump(self.Map, File)

	def Load(self):
		self.Map=shared.MapLoader.Map.config
		self.MapConfig=self.Map["Map"]
		self.TerrainConfig=self.Map["Terrain"]
		self.DecoratorConfig=self.Map["Decorator"]
		self.UnitConfig=self.Map["Units"]

	# def checkYourPrivileges(self):
	# 	if len(self.TerrainConfig)>1:
	# 		print(self.TerrainConfig["Heightmap"]["Scale"]+"test")
	# 	else:
	# 		print("Shit is cahs!")
	# 	#reactor.callLater(1, self.checkYourPrivileges)