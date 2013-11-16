from engine import shared, debug
from astar import AStar, AStarNode
from math import sqrt
from itertools import product

#if shared.side!="Server":
#	import ogre.renderer.OGRE as ogre

class AStarGrid(AStar):
	def heuristic(self, node, start, end):
		return sqrt((end.x - node.x)**2 + (end.y - node.y)**2)

class AStarGridNode(AStarNode):
	def __init__(self, x, y):
		self.x, self.y = x, y
		super(AStarGridNode, self).__init__()

	def move_cost(self, other):
		diagonal = abs(self.x - other.x) == 1 and abs(self.y - other.y) == 1
		return 14 if diagonal else 10

	def __repr__(self):
		return str((self.x, self.y))

class AStarGraph():
	def __init__(self):
		#debug.ACC("generateGraph", self.GetNextCoord, args=2, info="Get next point in the path")
		debug.ACC("a*_setcost", self.setNodeCost2, args=3, info="Set node cost\nUsage: x y cost")

	def generateGraph(self, mapscale, scale):
		"""Generates an complete Graph with the specified dimensions"""
		print("Generating A* Graph..")
		self.localscale = (mapscale / scale)+1
		self.mapscale = mapscale
		self.scale = scale
		self.realscale = float(float(self.mapscale) / float(self.localscale))
		print("A* Mapscale=%d | Scale=%d | Localscale=%d | Realscale=%f" % (self.mapscale, self.scale, self.localscale, self.realscale))

		self.nodes = [[AStarGridNode(x, y) for y in range(self.localscale)] for x in range(self.localscale)]
		self.totnodes = []
		self.graph = {}
		for x, y in product(range(self.localscale), range(self.localscale)):
			node = self.nodes[x][y]
			self.totnodes.append(node)
			self.graph[node] = []
			for i, j in product([-1, 0, 1], [-1, 0, 1]):
				if not (0 <= x + i < self.localscale): continue
				if not (0 <= y + j < self.localscale): continue
				self.graph[self.nodes[x][y]].append(self.nodes[x+i][y+j])
		return self.graph, self.nodes

	def regenerateGraph(self, mapscale, scale, nodes):
		"""Regenerates an complete Graph with the specified dimensions and with the specified exsisting set of nodes"""
		print("Regenerating A* Graph..")
		self.localscale = (mapscale / scale)+1
		self.mapscale = mapscale
		self.scale = scale
		self.realscale = float(float(self.mapscale) / float(self.localscale))
		print("A* Mapscale=%d | Scale=%d | Localscale=%d | Realscale=%f" % (self.mapscale, self.scale, self.localscale, self.realscale))

		self.nodes = nodes
		self.totnodes = []
		self.graph = {}
		for x, y in product(range(self.localscale), range(self.localscale)):
			node = self.nodes[x][y]
			self.totnodes.append(node)
			self.graph[node] = []
			for i, j in product([-1, 0, 1], [-1, 0, 1]):
				if not (0 <= x + i < self.localscale): continue
				if not (0 <= y + j < self.localscale): continue
				self.graph[self.nodes[x][y]].append(self.nodes[x+i][y+j])
		return self.graph, self.nodes

	def generateSearchGrid(self):
		"""Creates an Grid with the generated Graph"""
		self.grid = AStarGrid(self.graph)

	def getNode(self, x, y):
		"""Returns the node at that grid position"""
		if x>self.localscale-1:
			x = self.localscale-1
			shared.DPrint("AStar", 2, "getNode: Position out of bounds! Clamping to localscale")
		if y>self.localscale-1:
			y = self.localscale-1
			shared.DPrint("AStar", 2, "getNode: Position out of bounds! Clamping to localscale")

		return self.nodes[x][y]

	def getNodeAtWPos(self, x, y):
		"""Returns the node at that world position"""
		#nx = int( (float(float(x) / float(self.mapscale)) * float(float(self.localscale) / float(100)))*float(100) )
		#ny = int( (float(float(y) / float(self.mapscale)) * float(float(self.localscale) / float(100)))*float(100) )
		nx = int(round(float(x) / float(self.realscale)))
		ny = int(round(float(y) / float(self.realscale)))
		#print "(%d, %d)" % (nx, ny)
		return self.getNode(nx, ny)

	def convertLPosToWPos(self, x, y):
		"""Returns the worldpos for that localpos"""
		nx = int( (float(float(x) * float(self.realscale))))
		ny = int( (float(float(y) * float(self.realscale))))
		#print "(%d, %d)" % (nx, ny)
		return (nx, ny)

	def setNodeCost(self, node, cost):
		"""Sets the nodes current and default cost"""
		node.c = cost
		node.dc = cost

	def setNodeCost2(self, x, y, cost):
		self.setNodeCost(self.getNodeAtWPos(int(x), int(y)), int(cost))

	def setNodeWalkable(self, node, walkable):
		"""Sets if the node is walkable or not"""
		if walkable:
			node.c = node.dc
		else:
			node.c = 1000

	def setNodeType(self, node, nodetype):
		node.type = nodetype
			
	def Search(self, start, end, allowedtypes=[0]):
		"""Takes an endnode and an startnode, returns all the nodes required to traverse to get to the goal"""
		print("Searching grid...")
		for node in self.totnodes:
			node.g = 0
			node.h = 0
			node.parent = None
		return self.grid.search(start, end, allowedtypes=allowedtypes)

	def Search2(self, start, end, allowedtypes=[0]):
		"""Takes an startpos WORLD(x,y) and an endpos, returns a list of WORLD positions required to traverse to get to the goal"""
		print("Getting path between node at: %r (%d, %d) and node: %r (%d, %d)" % (self.getNodeAtWPos(start[0], start[1]), start[0], start[1], self.getNodeAtWPos(end[0], end[1]), end[0], end[1]))
		path = self.Search(self.getNodeAtWPos(start[0], start[1]), self.getNodeAtWPos(end[0], end[1]), allowedtypes=allowedtypes)
		print("Found path, converting to coordpath...")
		coordpath = []

		for node in path:
			coordpath.append((node.x*self.realscale, node.y*self.realscale))

		return coordpath