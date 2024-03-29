class AStar(object):
	def __init__(self, graph):
		self.graph = graph
		
	def heuristic(self, node, start, end):
		raise NotImplementedError
		
	def search(self, start, end):
		openset = set()
		closedset = set()
		current = start
		openset.add(current)
		while openset:

			#Select the node with the lowest g and h score
			current = min(openset, key=lambda o:o.g + o.h)
			if current == end:
				path = []
				while current.parent:
					#print("Current parent")
					path.append(current)
					c2 = current
					current = current.parent
					print "Node: (%d, %d)" % (current.x, current.y)
					if c2 == current.parent:
						print("Oh shit")
						break
				path.append(current)
				return path[::-1]
			openset.remove(current)
			closedset.add(current)
			for node in self.graph[current]:
				if node in closedset:
					continue
				if node in openset:
					new_g = current.g + current.move_cost(node)
					if node.g > new_g:
						node.g = new_g
						node.parent = current
				else:
					node.g = current.g + current.move_cost(node)
					node.h = self.heuristic(node, start, end)
					node.parent = current
					openset.add(node)
		return None

class AStarNode(object):
	def __init__(self):
		self.g = 0
		self.h = 0
		self.c = 0
		self.parent = None
		
	def move_cost(self, other):
		raise NotImplementedError
