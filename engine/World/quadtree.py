#Worldmodule - quadtree (QuadTree datastructure management)
#Module containing a quadtree manager

from posalgo import Rectangle
from traceback import print_exc

class QuadTree():
	def __init__(self, plevel, rectangle, max_objects=10, max_levels=5):
		self.max_objects = max_objects
		self.max_levels = max_levels

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

	def autoProvisionObjects(self):
		for obj in self.objects:
			for index in self.getIndexesByRectangle(obj._qt_rectangleSize):
				self.nodes[index].insertObject(obj, obj._qt_rectangleSize)

		self.objects=[]

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

	def insertObject(self, obj, rectangleSize):
		# print("Hello, I'm inserting at level: %d" % self.level)
		obj._qt_rectangleSize = rectangleSize
		
		if not hasattr(obj, "_qt_memberof"):
			obj._qt_memberof=[]

		if self.nodes[0]==None:
			#If this node is at the bottom of the tree, just insert the object. No need for unnessesary extra checks
			self.objects.append(obj)
			obj._qt_memberof.append(self)
			# print("I am at the bottom, inserting at %s" % str(self.bounds))

			if self.max_objects!=-1 and len(self.objects) > self.max_objects:
				if self.level < self.max_levels or self.max_levels==-1:
					self.split()
					self.autoProvisionObjects()

		else:
			#If this node has subnodes, then search further down the tree.
			for qt in self.getIndexesByRectangle(rectangleSize):
				# print("Searching subnodes: %d" % qt)
				self.nodes[qt].insertObject(obj, rectangleSize)

	def removeObject(self, obj):
		for qt in obj._qt_memberof:
			try:
				qt.objects.remove(obj)
			except ValueError:
				print_exc()
		obj._qt_memberof = []

	def getAllObjectsInSameArea(self, obj, objecttype=None):
		for qt in obj._qt_memberof:
			for otherobj in qt.objects:
				if not objecttype:
					yield otherobj
				else:
					# print("QuadTree: Found object, checking instance")
					if isinstance(otherobj, objecttype):
						# print("QuadTree: Correct instance")
						yield otherobj