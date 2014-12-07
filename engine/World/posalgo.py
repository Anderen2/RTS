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
			self.x = float(a)
			self.y = float(b)
			self.width = float(c)
			self.height = float(d)

		else:
			self.width = float(a)
			self.height = float(b)
			self.x = float(0)
			self.y = float(0)

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
		return "Rectangle: x:%f, y:%f (h:%f x w:%f)" % (self.x, self.y, self.height, self.width)

	def getWidth(self):
		#return (self.sides[3] - self.sides[1])
		return float(self.width)

	def getHeight(self):
		#return (self.sides[2] - self.sides[0])
		return float(self.height)

	def getX(self):
		return float(self.x)

	def getY(self):
		return float(self.y)