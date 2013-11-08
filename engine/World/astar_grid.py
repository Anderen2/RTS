from engine import shared, debug
from astar import AStar, AStarNode
from math import sqrt
from itertools import product

if shared.side!="Server":
	import ogre.renderer.OGRE as ogre

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
		self.mapscale = mapscale
		self.scale = scale
		self.localscale = mapscale / scale
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

	def generateSearchGrid(self):
		"""Creates an Grid with the generated Graph"""
		self.grid = AStarGrid(self.graph)

	def getNode(self, x, y):
		"""Returns the node at that grid position"""
		return self.nodes[x][y]

	def getNodeAtWPos(self, x, y):
		"""Returns the node at that world position"""
		nx = int( (float(float(x) / float(self.mapscale)) * float(float(self.localscale) / float(100)))*float(100) )
		ny = int( (float(float(y) / float(self.mapscale)) * float(float(self.localscale) / float(100)))*float(100) )
		print "(%d, %d)" % (nx, ny)
		return self.getNode(nx, ny)

	def setNodeCost(self, node, cost):
		"""Sets the nodes current and default cost"""
		node.c = cost
		node.dc = cost

	def setNodeCost2(self, x, y, cost):
		self.setNodeCost(self.getNode(int(x), int(y)), int(cost))

	def setNodeWalkable(self, node, walkable):
		"""Sets if the node is walkable or not"""
		if walkable:
			node.c = node.dc
		else:
			node.c = 99999

	def calculateSceneNodeCost(self, ogrescenenode):
		AABB = ogrescenenode._getWorldAABB()
		xyz1 = AABB.getCorner(ogre.AxisAlignedBox.FAR_LEFT_BOTTOM)
		xyz2 = AABB.getCorner(ogre.AxisAlignedBox.NEAR_RIGHT_BOTTOM)

		xy1 = (xyz1.x, xyz1.z)
		xy2 = (xyz2.x, xyz2.z)

		CoordinateRange = []

		for x in range(int(xy1[0]), int(xy2[0]+1)):
			for y in range(int(xy1[1]), int(xy2[1]+1)):
				CoordinateRange.append((x, y))

		#print("%s xy1" % (str(xy1)))
		#print("%s xy2" % (str(xy2)))
		#print("%d px2" % (len(CoordinateRange)))

		print("Setting coord..")
		for coord in CoordinateRange:
			self.setNodeWalkable(self.getNodeAtWPos(coord[0], coord[1]), False)
			pass

	def Search(self, start, end):
		"""Takes an endnode and an startnode, returns all the nodes required to traverse to get to the goal"""
		print("Searching grid...")
		for node in self.totnodes:
			node.g = 0
			node.h = 0
		return self.grid.search(start, end)

	def Search2(self, start, end):
		"""Takes an startpos WORLD(x,y) and an endpos, returns a list of WORLD positions required to traverse to get to the goal"""
		print("Getting path between node at: %r (%d, %d) and node: %r (%d, %d)" % (self.getNodeAtWPos(start[0], start[1]), start[0], start[1], self.getNodeAtWPos(end[0], end[1]), end[0], end[1]))
		path = self.Search(self.getNodeAtWPos(start[0], start[1]), self.getNodeAtWPos(end[0], end[1]))
		print("Found path, converting to coordpath...")
		coordpath = []

		for node in path:
			coordpath.append((node.x*self.scale, node.y*self.scale))

		return coordpath