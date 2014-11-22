#Worldmodule - quadtree (QuadTree datastructure management)
#Module containing a quadtree manager

from posalgo import Rectangle

class QuadTree():
	def __init__(self, plevel, rectangle):
		self.max_objects = 10
		self.max_levels = 5

		self.level = plevel
		self.bounds = rectangle

		self.objects = []

		self.nodes = [None]*4
		# self.split()

	def __getitem__(self, i):
		return self.nodes[i]

	def clear(self):
		self.objects = []

		for node in self.nodes:
			if node!=None:
				node.clear()
				del node

	def split(self):
		# subWidth = (self.bounds[3]-self.bounds[1])/2
		# subHeight = (self.bounds[2]-self.bounds[0])/2
		# x = self.position[0]
		# y = self.position[1]
		subWidth = self.bounds.getWidth() / 2
		subHeight = self.bounds.getHeight() / 2
		x = self.bounds.getX()
		y = self.bounds.getY()

		self.nodes[0] = QuadTree(self.level+1, Rectangle(x, y, subWidth, subHeight))
		self.nodes[1] = QuadTree(self.level+1, Rectangle(x + subWidth, y, subWidth, subHeight))
		self.nodes[2] = QuadTree(self.level+1, Rectangle(x, y + subHeight, subWidth, subHeight))
		self.nodes[3] = QuadTree(self.level+1, Rectangle(x + subWidth, y + subHeight, subWidth, subHeight))

	#Get single Index

	def getIndexByRectangle(self, rectangle):
		index = []
		verticalMidpoint = self.bounds.getX() + (self.bounds.getWidth() / 2)
		horizontalMidpoint = self.bounds.getY() + (self.bounds.getHeight() / 2)

		# Object can completely fit within the top quadrants
		topQuadrant = (rectangle.getY() < horizontalMidpoint and rectangle.getY() + rectangle.getHeight() < horizontalMidpoint)
		# Object can completely fit within the bottom quadrants
		bottomQuadrant = (rectangle.getY() > horizontalMidpoint)

		# Object can completely fit within the left quadrants
		if (rectangle.getX() < verticalMidpoint and rectangle.getX() + rectangle.getWidth() < verticalMidpoint):
			if (topQuadrant):
				index.append(0)

			if (bottomQuadrant):
				index.append(2)
		
		# Object can completely fit within the right quadrants
		if (rectangle.getX() > verticalMidpoint):
			if (topQuadrant):
				index.append(1)

			if (bottomQuadrant):
				index.append(3)


		return index

	def getIndexByPoint(self, point):
		index = None
		verticalMidpoint = self.bounds.getX() + (self.bounds.getWidth() / 2)
		horizontalMidpoint = self.bounds.getY() + (self.bounds.getHeight() / 2)

		# Object can completely fit within the top quadrants
		topQuadrant = (point[1] < horizontalMidpoint)
		# Object can completely fit within the bottom quadrants
		bottomQuadrant = (point[1] > horizontalMidpoint)

		# Object can completely fit within the left quadrants
		if (point[0] < verticalMidpoint):
			if (topQuadrant):
				index = 0

			if (bottomQuadrant):
				index = 2
		
		# Object can completely fit within the right quadrants
		if (point[0] > verticalMidpoint):
			if (topQuadrant):
				index = 1

			if (bottomQuadrant):
				index = 3


		return index

	def getIndexesByRectangle(self, rectangle):
		index = []
		verticalMidpoint = self.bounds.getX() + (self.bounds.getWidth() / 2)
		horizontalMidpoint = self.bounds.getY() + (self.bounds.getHeight() / 2)

		# Object can completely fit within the top quadrants
		#topQuadrant = (rectangle.getY() <= horizontalMidpoint) or (rectangle.getY() + rectangle.getHeight() <= horizontalMidpoint)
		topQuadrant = (rectangle.getY() <= horizontalMidpoint)
		bottomQuadrant = (rectangle.getY() + rectangle.getHeight() >= horizontalMidpoint)
		# Object can completely fit within the bottom quadrants
		#bottomQuadrant = (rectangle.getY() >= horizontalMidpoint) or (rectangle.getY() + rectangle.getHeight() <= horizontalMidpoint)

		# Object can completely fit within the left quadrants
		if (rectangle.getX() <= verticalMidpoint):
			if (topQuadrant):
				index.append(0)

			if (bottomQuadrant):
				index.append(2)
		
		# Object can completely fit within the right quadrants
		if (rectangle.getX() + rectangle.getWidth() >= verticalMidpoint):
			if (topQuadrant):
				index.append(1)

			if (bottomQuadrant):
				index.append(3)


		return index
