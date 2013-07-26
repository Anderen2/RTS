#Clientside otherplayer
from engine import shared, debug
from random import randrange

class Player():
	def __init__(self, UID, Username, PickledExtras):
		self.PlayerInfo={"Land":"Not Implemented!"}
		self.team=randrange(1,2,1)
		self.UID=UID
		self.username=Username

		self.Units=[]
