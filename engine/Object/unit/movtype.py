from engine import shared, debug
from moveable import Moveable

#Moveable Type-dependant Unitgroups
class Worker(Moveable):
	def init(self):
		self.type=1

class Vehicle(Moveable):
	def init(self):
		self.type=2

class Infantry(Moveable):
	def init(self):
		self.type=3

class Aircraft(Moveable):
	def init(self):
		self.type=4
		self.entity.Translate(0,100,0)

class Marine(Moveable):
	def init(self):
		self.type=5

class Other(Moveable):
	def init(self):
		self.type=0