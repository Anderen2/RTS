#cl_netOPlayer
from engine import shared, debug
class Player():
	def __init__(self, decoded):
		self.name=decoded["name"]
		self.ID=decoded["ID"]
		shared.objectManager.addEntry(100, self.ID, self)
		shared.DPrint("client", 0, str(self.ID)+"."+self.name+" joined!")