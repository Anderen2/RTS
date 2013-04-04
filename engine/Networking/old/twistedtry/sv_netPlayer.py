#sv_netPlayer
from engine import shared, debug
class Player():
	def __init__(self, name, ID, proto):
		shared.objectManager.addEntry(100, ID, self)
		self.name=name
		self.ID=ID
		self.protocol=proto
		self.PlayerInfo={
		'name':name,
		'ID':ID,
		'country':"Norway",
		'faction':0,
		'team':0
		}

	def getInfo(self):
		self.PlayerInfo={
		'name':self.name,
		'ID':self.ID,
		'country':"Norway",
		'faction':0,
		'team':0
		}
		return self.PlayerInfo