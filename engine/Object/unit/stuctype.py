from engine import shared, debug
from structure import Structure

#Structure Type-dependant Unitgroups
class Buildable(Structure):
	def init(self):
		self.type=1

class Bunker(Structure):
	def init(self):
		self.type=2

class Tech(Structure):
	def init(self):
		self.type=3