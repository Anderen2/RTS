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

		# 1. Begin at the starting point A and add it to an "open list" of nodes to be considered.
		# The open list is kind of like a shopping list. Right now there is just one item on the list, 
		# but we will have more later. It contains nodes that might fall along the path you want to take, but maybe not. 
		# Basically, this is a list of nodes that need to be checked out.   

		while openset:

			#Select the node with the lowest g and h score
			current = min(openset, key=lambda o:o.g + o.h)

			#If we have hit the end
			if current == end:
				path = []

				#Trace the path by walking backwards through the parents of the current node
				print("Found end, tracing path")
				while current.parent:
					# print("Current parent")
					c2 = current
					path.append(current)
					current = current.parent
					# print "Node: (%d, %d)" % (current.x, current.y)
					if c2 == current.parent:
						print("Oh shit")
						break

				path.append(current)
				return path[::-1]


			# 3. Drop the starting square A from your open list, and add it to a "closed list" of squares that you don't need to look at again for now. 
			openset.remove(current)
			closedset.add(current)



			for node in self.graph[current]:
				if node in closedset or node.c>9999:
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
