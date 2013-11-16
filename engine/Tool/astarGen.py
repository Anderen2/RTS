#AStar Graph Generator
#This module contains methods of manipulating, and automaticly generating the current A* Graph

from engine import shared, debug
import ogre.renderer.OGRE as ogre
import pickle

class aStarGenerators():
	def __init__(self):
		self.AStar = shared.Pathfinder.aStarPath

		debug.ACC("a*_clear", self.clearGraph, args=0, info="Clears all cost from the entire a* graph")
		debug.ACC("a*_gendec", self.generateDecorators, args=0, info="Regenerates nonwalkable areas due to decorator placement")
		debug.ACC("a*_genwater", self.generateWater, args=0, info="Regenerates nonwalkable areas due to water elevation")

		debug.ACC("a*_save", self.saveGraph, args=1, info="Save the current a* graph as an file\nUsage: a*_save filename")
		debug.ACC("a*_load", self.loadGraph, args=1, info="Load an a* graph from an file\nUsage: a*_load filename")

	def clearGraph(self):
		shared.DPrint("a*gen", 0, "Clearing current graph (%d nodes)" % (len(self.AStar.totnodes)))
		for node in self.AStar.totnodes:
			node.c = 0
			node.dc = 0

	def generateDecorators(self):
		DecoratorManager = shared.decHandeler

		for ID, Deco in DecoratorManager.decorators.items():
			self.calculateSceneNodeCost(Deco.entity.node)

	def generateHills(self, factor):
		#Cannot be preloaded? This differs between what node you are going from, there may be a node which are accessable from the left, but got a steep hill at the right.
		TerrainManager = shared.render3dTerrain

		for node in self.AStar.totnodes:
			nodewpos = self.AStar.convertLPosToWPos(node.x, node.y)
			altitude = TerrainManager.getHeightAtPos(nodewpos.x, nodewpos.y)
			self.AStar.setNodeCost(node, altitude)

	def generateWater(self):
		for node in self.AStar.totnodes:
			nodewpos = self.AStar.convertLPosToWPos(node.x, node.y)
			waterAtPos = shared.WaterManager.waterAtPos(nodewpos[0], nodewpos[1])
			if waterAtPos:
				self.AStar.setNodeType(node, 1)
			#altitude = TerrainManager.getHeightAtPos(nodewpos.x, nodewpos.y)

	def saveGraph(self, filename):
		with open(filename, "w") as f:
			pickle.dump(self.AStar.nodes, f)

	def loadGraph(self, filename):
		with open(filename, "r") as f:
			nodes = pickle.load(f)
			self.AStar.regenerateGraph(1500, 30, nodes)

	def calculateSceneNodeCost(self, ogrescenenode):
		AABB = ogrescenenode._getWorldAABB()
		xyz1 = AABB.getCorner(ogre.AxisAlignedBox.FAR_LEFT_BOTTOM)
		xyz2 = AABB.getCorner(ogre.AxisAlignedBox.NEAR_RIGHT_BOTTOM)

		xy1 = (xyz1.x, xyz1.z)
		xy2 = (xyz2.x, xyz2.z)

		CoordinateRange = []

		for x in xrange(int(xy1[0]), int(xy2[0]+1)):
			for y in xrange(int(xy1[1]), int(xy2[1]+1)):
				CoordinateRange.append((x, y))

		#print("%s xy1" % (str(xy1)))
		#print("%s xy2" % (str(xy2)))
		#print("%d px2" % (len(CoordinateRange)))

		print("Setting coord..")
		for coord in CoordinateRange:
			if coord[0]<self.AStar.mapscale and coord[1]<self.AStar.mapscale:
				node = self.AStar.getNodeAtWPos(coord[0], coord[1])
				self.AStar.setNodeWalkable(node, False)
				self.AStar.setNodeType(node, 2)