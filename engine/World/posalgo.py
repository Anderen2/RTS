#Worldmodule - posalgo (Positional Algorithms)
#Module containing different positional algorithms

def in_circle(center_x, center_y, radius, x, y):
		square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
		return square_dist <= radius ** 2

class Rectangle():
	""" a stripped out class for 3D vectors"""
	
	__class__="Rectangle"

	def __init__(self, a, b, c=None, d=None):
		if c!=None and d!=None:
			self.x = a
			self.y = b
			self.width = c
			self.height = d

		else:
			self.width = a
			self.height = b
			self.x = 0
			self.y = 0

	def __getitem__(self,i):
		return self.sides[i]
	
	def __mul__(self,s):
		pass

	def __div__(self,s):
		pass

	def __add__(self,A):
		pass
	
	def __sub__(self,A):
		pass

	def __cmp__(self,v):
		pass

	def __iter__(self):
		return self.sides.__iter__()
	
	def __eq__(self,v):
		if (self.sides==v):
			return True
		return False
	
	def __str__(self):
		return "Rectangle: x:%d, y:%d (h:%d x w:%d)" % (self.x, self.y, self.height, self.width)

	def getWidth(self):
		#return (self.sides[3] - self.sides[1])
		return self.width

	def getHeight(self):
		#return (self.sides[2] - self.sides[0])
		return self.height

	def getX(self):
		return self.x

	def getY(self):
		return self.y