#Clientside SelfPlayer
from twisted.internet import reactor

from engine import shared, debug
from engine.Networking import sh_netObject, sh_netMethod

class SelfPlayer():
	def __init__(self):
		self.username="Anderen2"
		self.PickledExtras=""
		self.ID=None
		shared.protocol.sendMethod(2, "HI", [self.username, self.PickledExtras])
		shared.client.RetMeBack(self.recv_HI, "HI")

	def recv_HI(self, ID):
		self.ID=ID