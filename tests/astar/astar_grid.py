from astar import AStar, AStarNode
from math import sqrt

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

class AStarGraph():
	def __init__(self):
		#debug.ACC("generateGraph", self.GetNextCoord, args=2, info="Get next point in the path")
		debug.ACC("a*_setcost", self.setNodeCost2, args=3, info="Set node cost\nUsage: x y cost")

	def generateGraph(self, mapinfo):
		"""Generates an complete Graph with the specified dimensions"""
		self.nodes = [[AStarGridNode(x, y) for y in range(mapinfo["height"])] for x in range(mapinfo["width"])]
		self.graph = {}
		for x, y in product(range(mapinfo["width"]), range(mapinfo["height"])):
			node = self.nodes[x][y]
			self.graph[node] = []
			for i, j in product([-1, 0, 1], [-1, 0, 1]):
				if not (0 <= x + i < mapinfo["width"]): continue
				if not (0 <= y + j < mapinfo["height"]): continue
				self.graph[self.nodes[x][y]].append(self.nodes[x+i][y+j])
		return self.graph, self.nodes

	def generateSearchGrid(self):
		"""Creates an Grid with the generated Graph"""
		self.grid = AStarGrid(self.graph)

	def getNode(self, x, y):
		"""Returns the node at that position"""
		return self.nodes[x][y]

	def setNodeCost(self, node, cost):
		"""Sets the nodes current and default cost"""
		node.c = cost
		node.dc = cost

	def setNodeCost2(self, x, y, cost):
		setNodeCost(getNode(int(x), int(y)), cost)

	def setNodeWalkable(self, node, walkable):
		"""Sets if the node is walkable or not"""
		if walkable:
			node.c = node.dc
		else:
			node.c = 99999

	def Search(self, start, end):
		"""Takes an endnode and an startnode, returns all the nodes required to traverse to get to the goal"""
		return self.grid.search(start, end)

	def Search2(self, start, end):
		"""Takes an startpos (x,y) and an endpos, returns a list of positions required to traverse to get to the goal"""
		path = self.Search(self.getNode(start[0], start[1]), self.getNode[end[0], end[1]])
		coordpath = []

		for node in path:
			coordpath.append((node.x, node.y))

		return coordpath