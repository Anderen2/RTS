from astar_grid import AStarGrid, AStarGridNode
from itertools import product

def make_graph(mapinfo):
	nodes = [[AStarGridNode(x, y) for y in range(mapinfo["height"])] for x in range(mapinfo["width"])]
	graph = {}
	for x, y in product(range(mapinfo["width"]), range(mapinfo["height"])):
		node = nodes[x][y]
		graph[node] = []
		for i, j in product([-1, 0, 1], [-1, 0, 1]):
			if not (0 <= x + i < mapinfo["width"]): continue
			if not (0 <= y + j < mapinfo["height"]): continue
			graph[nodes[x][y]].append(nodes[x+i][y+j])
	return graph, nodes

print("Creating Graph")
graph, nodes = make_graph({"width": 512, "height": 512})
print("paths")
print(graph[nodes[49][40]])
# nodes[49][39].c = 99
# nodes[49][40].c = 99
# nodes[50][39].c = 999
# nodes[49][41].c = 90
# nodes[51][39].c = 90
# nodes[50][41].c = 90
# nodes[51][41].c = 90
# nodes[51][40].c = 90

paths = AStarGrid(graph)
start, end = nodes[50][40], nodes[1][1]
print("search")
path = paths.search(start, end)

start, end = nodes[1][1], nodes[190][500]
print("search")
path = paths.search(start, end)

start, end = nodes[190][500], nodes[500][60]
print("search")
path = paths.search(start, end)

if path is None:
	print "No path found"
else:
	print "Path found:"
	for node in path:
		print "(%d,%d) = [g: %d, h: %d, c: %d, t: %d]" % (node.x, node.y, node.g, node.h, node.c, node.g+node.h)
