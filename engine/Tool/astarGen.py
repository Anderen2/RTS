#AStar Graph Generator
#This module contains methods of manipulating, and automaticly generating the current A* Graph

from engine import shared, debug
import pickle

class aStarGenerators():
	def __init__(self):
		self.AStar = shared.Pathfinder.aStarPath

		debug.ACC("a*_clear", self.clearGraph, args=0, info="Clears all cost from the entire a* graph")
		debug.ACC("a*_gendec", self.generateDecorators, args=0, info="Regenerates nonwalkable areas due to decorator placement")

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
			self.AStar.calculateSceneNodeCost(Deco.entity.node)

	def generateHills(self, factor):
		#Cannot be preloaded? This differs between what node you are going from, there may be a node which are accessable from the left, but got a steep hill at the right.
		TerrainManager = shared.render3dTerrain

		for node in self.AStar.totnodes:
			nodewpos = self.AStar.convertLPosToWPos(node.x, node.y)
			altitude = TerrainManager.getHeightAtPos(nodewpos.x, nodewpos.y)
			self.AStar.setNodeCost(node, altitude)

	def saveGraph(self, filename):
		with open(filename, "w") as f:
			pickle.dump(self.AStar.nodes, f)

	def loadGraph(self, filename):
		with open(filename, "r") as f:
			nodes = pickle.load(f)
			self.AStar.regenerateGraph(1500, 30, nodes)