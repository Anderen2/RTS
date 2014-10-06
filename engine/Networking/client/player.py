#Clientside otherplayer
from engine import shared, debug

class Player():
	def __init__(self, UID, Username, Team, Extras):
		self.PlayerInfo=Extras
		self.team=Team
		self.UID=UID
		self.username=Username
		self.color=Extras["color"]
		self.yourself = False

		self.Units=[]

	def Think(self, delta):
		for unit in self.Units:
			unit._think(delta)
