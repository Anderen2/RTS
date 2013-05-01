#Serverside Player
from engine import debug, shared

class Player():
	def __init__(self, UID, Username, Protocol, PickledExtras):
		#self.PlayerInfo=pickle.loads(PickledExtras)
		self.PlayerInfo={"Land":"Of the dead"}
		self.UID=UID
		self.username=Username
		self.Protocol=Protocol
		shared.ChatManager.addMember(self.UID, 1)