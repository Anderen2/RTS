#cl_netPlayer
from random import randrange
from engine import shared, debug


class Player():
	def __init__(self):
		shared.objectManager.addEntry(0, 0, self)

		self.name="Anderen2"+str(randrange(0,100,1))

	def HI(self, ID, Protocol=None):
		self.ID=int(ID)
		print("Got ID: "+str(ID))