#cl_netPlayer
from engine import shared, debug
class Player():
	def __init__(self):
		shared.objectManager.addEntry(0, 2, self)

	def HI(self, ID, Protocol=None):
		self.ID=int(ID)
		print("Got ID: "+str(ID))