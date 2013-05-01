#Clientside otherplayer
from engine import shared, debug

class Player():
	def __init__(self, UID, Username, PickledExtras):
		self.PlayerInfo={"Land":"Not Implemented!"}
		self.UID=UID
		self.username=Username
